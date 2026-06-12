def calculate_commission(req):
    return "0.25%" if req.is_heavy_deal else 100000
