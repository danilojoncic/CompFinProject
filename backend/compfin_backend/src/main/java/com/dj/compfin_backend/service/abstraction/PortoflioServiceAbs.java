package com.dj.compfin_backend.service.abstraction;

import com.dj.compfin_backend.dto.CreatePortfolioDto;
import com.dj.compfin_backend.dto.ServiceResponse;
import com.dj.compfin_backend.model.Portfolio;

import java.util.Optional;

public interface PortoflioServiceAbs {
    ServiceResponse findPortfolioByName(String name);
    ServiceResponse createPortfolio(CreatePortfolioDto dto);
    ServiceResponse getPortfolioStatForDay(String portfolioName,String day);
    ServiceResponse getPortfolioStatTodate(String portfolioName,String day);
}
