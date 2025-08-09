package com.dj.compfin_backend.dto;

import com.dj.compfin_backend.model.Stock;

import java.util.Set;

public record PortfolioStats(String name, Set<Stock> stocks, double prctReturn) {
}
