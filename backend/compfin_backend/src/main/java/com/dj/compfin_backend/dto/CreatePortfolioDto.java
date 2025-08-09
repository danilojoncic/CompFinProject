package com.dj.compfin_backend.dto;

import java.util.List;
import java.util.Set;

public record CreatePortfolioDto(String name, List<String> tickers) {
}
