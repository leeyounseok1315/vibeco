def process_payment(order, payment_method):
    if payment_method=="신용카드":
        order["status"]="paid"
        return "결제 완료"
    else:
        order["status"]="failed"
        return "결제 실패"