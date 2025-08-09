package com.dj.compfin_backend.repository;

import com.dj.compfin_backend.model.StockPrice;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.util.List;

@Repository
public interface StockPriceRepository extends JpaRepository<StockPrice, Long> {
    List<StockPrice> findByStock_CompanyNameInAndDate(List<String> companyNames, LocalDate date);
    List<StockPrice> findByStock_CompanyNameInAndDateBetween(List<String> companyNames, LocalDate startDate, LocalDate endDate);
}
