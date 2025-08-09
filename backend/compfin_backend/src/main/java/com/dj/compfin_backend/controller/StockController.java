package com.dj.compfin_backend.controller;

import com.dj.compfin_backend.dto.ServiceResponse;
import com.dj.compfin_backend.service.StockService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/stock")
@RequiredArgsConstructor
public class StockController {
    private final StockService stockService;

    @GetMapping("/all")
    public ResponseEntity<?> getAllStocksInfo() {
        ServiceResponse sr = stockService.getAllStock();
        return ResponseEntity.status(sr.code()).body(sr.data());
    }


    @GetMapping("ticker/{ticker}")
    public ResponseEntity<?> getStock(@PathVariable String ticker) {
        ServiceResponse sr = stockService.getStock(ticker);
        return ResponseEntity.status(sr.code()).body(sr.data());
    }

}
