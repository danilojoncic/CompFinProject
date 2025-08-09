package com.dj.compfin_backend.controller;
import com.dj.compfin_backend.dto.CreatePortfolioDto;
import com.dj.compfin_backend.dto.ServiceResponse;
import com.dj.compfin_backend.service.PortfolioService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/portfolio")
@RequiredArgsConstructor
public class PortfolioController {
    private final PortfolioService portfolioService;


    @GetMapping("/{name}")
    public ResponseEntity<?> getPortfolio(@PathVariable String name) {
        ServiceResponse sr = portfolioService.findPortfolioByName(name);
        return ResponseEntity.status(sr.code()).body(sr);
    }


    @PostMapping("/create")
    public ResponseEntity<?> createPortfolio(@RequestBody CreatePortfolioDto dto) {
        ServiceResponse sr = portfolioService.createPortfolio(dto);
        return ResponseEntity.status(sr.code()).body(sr);
    }

    @GetMapping("/stat/{portfolio}/{date}")
    public ResponseEntity<?> getPortfolioStatForADay(
            @PathVariable String portfolio,
            @PathVariable String date) {
        ServiceResponse sr = portfolioService.getPortfolioStatForDay(portfolio, date);
        return ResponseEntity.status(sr.code()).body(sr.data());
    }

    @GetMapping("/stat/todate/{portfolio}/{date}")
    public ResponseEntity<?> getPortfolioStatToToday(
            @PathVariable String portfolio,
            @PathVariable String date) {
        ServiceResponse sr = portfolioService.getPortfolioStatTodate(portfolio, date);
        return ResponseEntity.status(sr.code()).body(sr.data());
    }

    //yyyy-MM-dd

}
