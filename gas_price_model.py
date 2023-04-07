import math
import random
import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.stride_tricks import sliding_window_view
from scipy.stats import genextreme
from scipy.integrate import quad


def main():
    historical_gas_prices = generate_historical_gas_prices(1000, 400000, 100)
    
    max_base_fee = 150
    block_time_secs = 12
    coverage_period_days = 1
    coverage_period = round((coverage_period_days * 24 * 60 * 60) / block_time_secs)

    max_gas_prices = calculate_max_gas_prices(historical_gas_prices, coverage_period)
    probability_exceed_max_base_fee = calculate_probability_exceed_max_base_fee(max_gas_prices, max_base_fee)

    payout = 1000
    insurance_premium = calculate_insurance_premium(probability_exceed_max_base_fee, payout)

    print_statistics(max_gas_prices, insurance_premium)
    plot_gas_prices(historical_gas_prices, max_gas_prices, coverage_period_days)

    params = genextreme.fit(max_gas_prices)
    x_values, pdf_values = calculate_pdf_values(params, max_gas_prices)

    expected_payoff = calculate_expected_payoff(params, payoff_start=max_base_fee)
    print(f"Expected payoff: {expected_payoff:.2f}")

    plot_histogram_and_fitted_pdf(max_gas_prices, x_values, pdf_values)


def generate_historical_gas_prices(start_block, end_block, mean_gas):
    gas_walk = [mean_gas]
    for i in range(1, end_block - start_block):
        gas_walk.append(gas_walk[i-1] * (1.125 if random.random() < math.exp(-gas_walk[i-1]/mean_gas) else 0.875))
    return np.array(gas_walk)


def calculate_max_gas_prices(historical_gas_prices, coverage_period):
    return np.max(sliding_window_view(historical_gas_prices, window_shape=coverage_period), axis=1)


def calculate_probability_exceed_max_base_fee(max_gas_prices, max_base_fee):
    exceed_max_base_fee_count = sum(1 for price in max_gas_prices if price > max_base_fee)
    return exceed_max_base_fee_count / len(max_gas_prices)


def calculate_insurance_premium(probability_exceed_max_base_fee, payout, admin_cost_and_profit_markup=0.15):
    return (probability_exceed_max_base_fee * payout) * (1 + admin_cost_and_profit_markup)


def print_statistics(max_gas_prices, insurance_premium):
    print(f"Mean: {np.mean(max_gas_prices):.2f} GWEI")
    print(f"Variance: {np.var(max_gas_prices):.2f} GWEI")
    print(f"Insurance Premium: {insurance_premium:.2f} GWEI")


def plot_gas_prices(historical_gas_prices, max_gas_prices, coverage_period_days):
    fig, (ax_hist, ax_max) = plt.subplots(2, 1)
    ax_hist.plot(np.arange(len(historical_gas_prices)), historical_gas_prices)
    ax_hist.set(title="Historical gas prices")

    ax_max.plot(np.arange(len(max_gas_prices)), max_gas_prices)
    ax_max.set(title=f"Maximum gas prices ({coverage_period_days} day window)")

    plt.tight_layout()
    plt.show()


def calculate_pdf_values(params, max_gas_prices):
    x_values = np.linspace(np.min(max_gas_prices), np.max(max_gas_prices), 1000)
    pdf_values = genextreme.pdf(x_values, *params)
    return x_values, pdf_values


def calculate_expected_payoff(params, payoff_start, payoff_end=10000):
    payoff_fn = lambda x: (x - payoff_start)

    def integrand(x, params):
        pdf = genextreme.pdf(x, *params)
        return payoff_fn(x) * pdf

    expected_payoff, _ = quad(integrand, payoff_start, payoff_end, args=(params,))
    return expected_payoff

def plot_histogram_and_fitted_pdf(max_gas_prices, x_values, pdf_values):
    plt.hist(max_gas_prices, bins=30, density=True, alpha=0.6, color='g', label='Histogram')
    plt.plot(x_values, pdf_values, 'r-', lw=2, label='Fitted PDF')
    plt.title('Maximum Gas Prices and Fitted Genextreme PDF')
    plt.xlabel('Maximum Gas Price')
    plt.ylabel('Probability Density')
    plt.legend(loc='best')
    plt.show()

if __name__ == "__main__":
    main()


