
def validate_not_mobile(value):
    
    phone = value
    if phone[0] == '0' and len(phone) == 10:
        return '254'+ phone[1:]
    elif phone[0] == '+':
        return phone[1:]
    