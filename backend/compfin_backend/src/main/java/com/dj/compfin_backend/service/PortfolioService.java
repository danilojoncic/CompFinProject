package com.dj.compfin_backend.service;

import com.dj.compfin_backend.dto.CreatePortfolioDto;
import com.dj.compfin_backend.dto.Message;
import com.dj.compfin_backend.dto.ServiceResponse;
import com.dj.compfin_backend.model.Portfolio;
import com.dj.compfin_backend.model.Stock;
import com.dj.compfin_backend.model.StockPrice;
import com.dj.compfin_backend.repository.PortfolioRepository;
import com.dj.compfin_backend.repository.StockPriceRepository;
import com.dj.compfin_backend.repository.StockRepository;
import com.dj.compfin_backend.service.abstraction.PortoflioServiceAbs;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Set;

@Service
@RequiredArgsConstructor
public class PortfolioService implements PortoflioServiceAbs {
    private final PortfolioRepository portfolioRepository;
    private final StockRepository stockRepository;
    private final StockPriceRepository stockPriceRepository;


    @Override
    public ServiceResponse findPortfolioByName(String name) {
        return portfolioRepository.findPortfolioByName(name)
                .map(portfolio -> new ServiceResponse(200,portfolio))
                .orElseGet(() -> new ServiceResponse(404,new Message("Portfolio not found")));
    }


    @Override
    public ServiceResponse createPortfolio(CreatePortfolioDto dto) {
        if (portfolioRepository.existsPortfolioByName(dto.name())) {
            return new ServiceResponse(401, new Message("Portfolio already exists"));
        }
        List<Stock> stocks = stockRepository.findByTickerIn(dto.tickers());
        if (stocks.size() != dto.tickers().size()) {
            return new ServiceResponse(400, new Message("Some stocks do not exist"));
        }
        Portfolio portfolio = new Portfolio(dto.name(), Set.copyOf(stocks));
        portfolioRepository.save(portfolio);
        return new ServiceResponse(201, portfolio);
    }

    @Override
    public ServiceResponse getPortfolioStatForDay(String portfolioName, String day) {
        LocalDate date = LocalDate.parse(day);
        Portfolio portfolio = portfolioRepository.findPortfolioByName(portfolioName)
                .orElseThrow(() -> new RuntimeException("Portfolio not found"));

        double dailyReturn = calculateDailyReturn(portfolio.getStocks(), date);

        return new ServiceResponse(200, Map.of("date", date, "dailyReturn", dailyReturn));
    }

    @Override
    public ServiceResponse getPortfolioStatTodate(String portfolioName, String startDay) {
        LocalDate startDate = LocalDate.parse(startDay);
        LocalDate endDate = LocalDate.now();

        Portfolio portfolio = portfolioRepository.findPortfolioByName(portfolioName)
                .orElseThrow(() -> new RuntimeException("Portfolio not found"));

        double totalReturn = calculateTotalReturn(portfolio.getStocks(), startDate, endDate);

        return new ServiceResponse(200, Map.of(
                "startDate", startDate,
                "endDate", endDate,
                "totalReturn", totalReturn
        ));
    }



    private double calculateReturnBetweenDates(Set<Stock> stocks, LocalDate fromDate, LocalDate toDate) {
        List<String> companyNames = stocks.stream()
                .map(Stock::getCompanyName)
                .toList();

        double fromValue = stockPriceRepository.findByStock_CompanyNameInAndDate(companyNames, fromDate)
                .stream()
                .mapToDouble(StockPrice::getClosePrice)
                .sum();

        double toValue = stockPriceRepository.findByStock_CompanyNameInAndDate(companyNames, toDate)
                .stream()
                .mapToDouble(StockPrice::getClosePrice)
                .sum();

        if (fromValue == 0) return 0;

        return ((toValue - fromValue) / fromValue) * 100.0;
    }

    private double calculateDailyReturn(Set<Stock> stocks, LocalDate day) {
        return calculateReturnBetweenDates(stocks, day.minusDays(1), day);
    }

    private double calculateTotalReturn(Set<Stock> stocks, LocalDate startDate, LocalDate endDate) {
        return calculateReturnBetweenDates(stocks, startDate, endDate);
    }




}
