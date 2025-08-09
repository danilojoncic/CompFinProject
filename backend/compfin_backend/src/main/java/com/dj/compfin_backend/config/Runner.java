package com.dj.compfin_backend.config;


import com.dj.compfin_backend.dto.StockDto;
import com.dj.compfin_backend.model.Portfolio;
import com.dj.compfin_backend.model.Stock;
import com.dj.compfin_backend.model.StockPrice;
import com.dj.compfin_backend.repository.PortfolioRepository;
import com.dj.compfin_backend.repository.StockPriceRepository;
import com.dj.compfin_backend.repository.StockRepository;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.apachecommons.CommonsLog;
import org.springframework.boot.CommandLineRunner;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Component;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.time.LocalDate;
import java.util.*;
import java.util.logging.Logger;
import java.util.stream.Collectors;

@Component
@RequiredArgsConstructor
public class Runner implements CommandLineRunner {

    private final PortfolioRepository portfolioRepository;
    private final StockRepository stockRepository;
    private final StockPriceRepository stockPriceRepository;
    Logger logger = Logger.getLogger(Runner.class.getName());
    private final ObjectMapper objectMapper;


    @Override
    public void run(String... args) throws Exception {
        if (stockRepository.count() == 0) {
            logger.info("Loading stocks from ticker_for_portfolio.json");
            ClassPathResource stockResource = new ClassPathResource("ticker_for_portfolio.json");
            try (InputStream is = stockResource.getInputStream()) {
                Map<String, String> stocks = objectMapper.readValue(is, new TypeReference<Map<String, String>>() {});
                stocks.forEach((ticker, companyName) -> {
                    Stock stock = new Stock(ticker, companyName);
                    stockRepository.save(stock);
                });
                logger.info("Stocks loaded.");
            } catch (Exception e) {
                logger.severe("Failed to load stocks: " + e.getMessage());
                throw e;
            }
        } else {
            logger.info("Stocks already loaded, skipping.");
        }

        if (portfolioRepository.count() == 0) {
            logger.info("Loading portfolios from portfolios.json");
            ClassPathResource portfolioResource = new ClassPathResource("100k_random_portfolios.json");
            try (InputStream is = portfolioResource.getInputStream()) {
                Map<String, java.util.List<StockDto>> portfolios = objectMapper.readValue(is,
                        new TypeReference<Map<String, java.util.List<StockDto>>>() {
                        });

                for (var entry : portfolios.entrySet()) {
                    String portfolioName = entry.getKey();
                    java.util.List<StockDto> stockDTOs = entry.getValue();

                    Set<Stock> stocks = stockDTOs.stream()
                            .map(dto -> stockRepository.findByTicker(dto.ticker())
                                    .orElseThrow(() -> new RuntimeException("Stock with ticker " + dto.ticker() + " not found")))
                            .collect(Collectors.toSet());

                    Portfolio portfolio = new Portfolio(portfolioName, stocks);
                    portfolioRepository.save(portfolio);
                }
                logger.info("Portfolios loaded.");
            } catch (Exception e) {
                logger.severe("Failed to load portfolios: " + e.getMessage());
                throw e;
            }
        } else {
            logger.info("Portfolios already loaded, skipping.");
        }

        if(stockPriceRepository.count() == 0){
            ClassPathResource resource = new ClassPathResource("without_nulls_stock_data.csv");
            logger.info("Reading stock data from file:");

            try (BufferedReader reader = new BufferedReader(new InputStreamReader(resource.getInputStream()))) {
                String header = reader.readLine();
                String[] columns = header.split(",");

                Map<String, int[]> tickerColumnMap = new HashMap<>();
                for (int i = 1; i < columns.length; i += 5) {
                    String colName = columns[i];
                    String ticker = colName.split("_")[0];
                    tickerColumnMap.put(ticker, new int[]{
                            i,     // Open
                            i + 1, // High
                            i + 2, // Low
                            i + 3, // Close
                            i + 4  // Volume
                    });
                }

                String line;
                List<StockPrice> buffer = new ArrayList<>();
                int batchSize = 1000;

                while ((line = reader.readLine()) != null) {
                    logger.info("Batch loaded!");

                    String[] values = line.split(",");
                    LocalDate date = LocalDate.parse(values[0]);

                    for (Map.Entry<String, int[]> entry : tickerColumnMap.entrySet()) {
                        String ticker = entry.getKey();
                        int[] idx = entry.getValue();

                        Stock stock = stockRepository.findByTicker(ticker)
                                .orElse(null);
                        if (stock == null) continue;

                        StockPrice price = new StockPrice();
                        price.setStock(stock);
                        price.setDate(date);
                        price.setOpenPrice(Double.valueOf(values[idx[0]]));
                        price.setHighPrice(Double.valueOf(values[idx[1]]));
                        price.setLowPrice(Double.valueOf(values[idx[2]]));
                        price.setClosePrice(Double.valueOf(values[idx[3]]));
                        price.setVolume(Long.valueOf(values[idx[4]]));

                        buffer.add(price);

                        if (buffer.size() >= batchSize) {
                            stockPriceRepository.saveAll(buffer);
                            buffer.clear();
                        }
                    }
                }

                if (!buffer.isEmpty()) {
                    stockPriceRepository.saveAll(buffer);
                }
            }
        }
        logger.info(stockPriceRepository.count() + " stock prices");
    }
}




