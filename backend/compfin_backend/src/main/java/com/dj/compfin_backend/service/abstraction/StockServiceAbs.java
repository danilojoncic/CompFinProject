package com.dj.compfin_backend.service.abstraction;

import com.dj.compfin_backend.dto.ServiceResponse;

public interface StockServiceAbs {
    ServiceResponse getAllStock();
    ServiceResponse getStock(String ticker);
}
