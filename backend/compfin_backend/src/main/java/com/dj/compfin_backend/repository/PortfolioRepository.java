package com.dj.compfin_backend.repository;

import com.dj.compfin_backend.model.Portfolio;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface PortfolioRepository extends JpaRepository<Portfolio, Long> {
    Optional<Portfolio> findPortfolioByName(String name);
    boolean existsPortfolioByName(String name);

}
