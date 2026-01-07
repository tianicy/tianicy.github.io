---
title: Django 框架入门指南
date: 2026-01-06
category: backends
tags: ['django', 'python']
reading_time: 5
---

# Django 框架入门指南

这是关于 Django 框架入门指南 的示例文章内容。

## 简介

本文将详细介绍 Django 框架入门指南 的相关知识和实践经验。

## 主要内容

1. 基础概念讲解
2. 实战案例演示
3. 最佳实践总结

## 代码示例

```python
from __future__ import annotations
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, unique
from typing import Optional

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")

# ---------- 1. 领域模型 ----------
@unique
class Channel(Enum):
    WECHAT = "WECHAT"
    ALIPAY = "ALIPAY"

@dataclass(slots=True)
class Order:
    order_id: str
    amount: float
    channel: Channel
    paid: bool = field(default=False)

    # 幂等令牌：相同 order_id + token 重复调用直接返回成功
    idempotent_token: str = field(default="")

# ---------- 2. 抽象接口 ----------
class PaymentGateway(ABC):
    """支付网关抽象：真正的钱从这里进出"""

    @abstractmethod
    def charge(self, order: Order) -> bool:
        """扣款，返回是否成功（网络超时/余额不足都算失败）"""
        raise NotImplementedError

    @property
    @abstractmethod
    def channel(self) -> Channel:
        raise NotImplementedError

# ---------- 3. 实现层（带异常 & 重试 & 幂等） ----------
class WeChatGateway(PaymentGateway):
    channel = Channel.WECHAT

    def charge(self, order: Order) -> bool:
        # 模拟：10% 概率网络抖动
        if time.time_ns() % 8 == 1:
            raise TimeoutError("微信网关超时")
        # 模拟：余额不足
        if order.amount > 1_000:
            logging.warning("微信：用户余额不足")
            return False
        logging.info("微信扣款成功")
        return True

class AliPayGateway(PaymentGateway):
    channel = Channel.ALIPAY

    def charge(self, order: Order) -> bool:
        # 支付宝偶尔“系统繁忙”
        if time.time_ns() % 8 == 0:
            logging.warning("支付宝：系统繁忙")
            return False
        logging.info("支付宝扣款成功")
        return True

# ---------- 4. 统一支付服务（应用层） ----------
class PaymentService:
    """对外唯一入口，屏蔽渠道差异，解决重试 & 幂等"""

    def __init__(self) -> None:
        self._gateways = {g.channel: g for g in [WeChatGateway(), AliPayGateway()]}
        # 本地简单内存幂等表（生产用 Redis / DB）
        self._idempotent_cache: set[str] = set()

    def pay(self, order: Order, max_retry: int = 5) -> bool:
        if order.paid:
            logging.info("订单已支付，直接返回")
            return True

        # 幂等校验
        key = f"{order.order_id}:{order.idempotent_token}"
        if key in self._idempotent_cache:
            logging.info("幂等命中，直接返回成功")
            return True

        gateway = self._gateways[order.channel]

        for attempt in range(1, max_retry + 1):
            try:
                ok = gateway.charge(order)
                if ok:
                    order.paid = True
                    self._idempotent_cache.add(key)
                    return True
                # 明确失败，不重试
                return False
            except TimeoutError as exc:
                logging.warning("第 %s 次超时: %s", attempt, exc)
                if attempt == max_retry:
                    return False
                time.sleep(0.5 * attempt)  # 指数退避

        return False

# ---------- 5. 客户端调用 ----------
if __name__ == "__main__":
    svc = PaymentService()

    o1 = Order("A123", 991, Channel.WECHAT, idempotent_token="tk1")
    o2 = Order("B456", 1500, Channel.ALIPAY, idempotent_token="tk2")  # 余额不足场景
    o3 = Order("A023", 99.9, Channel.WECHAT, idempotent_token="tk1")  # 重复提交

    for o in (o1, o2, o3):
        success = svc.pay(o)
        print(f"订单 {o.order_id} 支付结果: {'✅' if success else '❌'}\n")
```

## 总结

希望本文对你有所帮助！
