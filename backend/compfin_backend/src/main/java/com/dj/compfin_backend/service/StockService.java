package com.dj.compfin_backend.service;

import com.dj.compfin_backend.dto.Message;
import com.dj.compfin_backend.dto.ServiceResponse;
import com.dj.compfin_backend.repository.StockRepository;
import com.dj.compfin_backend.service.abstraction.StockServiceAbs;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class StockService implements StockServiceAbs {
    private final StockRepository stockRepository;
    @Override
    public ServiceResponse getAllStock() {
        return new ServiceResponse(200, stockRepository.findAll());
    }

    @Override
    public ServiceResponse getStock(String name) {
        return stockRepository.findByTicker(name)
                .map(stock -> new ServiceResponse(200,stock))
                .orElseGet(() -> new ServiceResponse(404,new Message("Stock Not Found")));
    }
}
