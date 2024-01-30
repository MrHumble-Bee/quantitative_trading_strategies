import pandas as pd
def generate_holdings_pnl(price1: pd.Series, price2: pd.Series, n_shares1: pd.Series, n_shares2: pd.Series, symbol1: str, symbol2: str, signal_series: pd.Series, trailing_stop: float=None):
    prev_signal = 0
    current_pos_pl = 0
    gross_entry_outlay = 0
    is_open_pos = False
    current_pl = 0
    share_holdings = {
        f'{symbol1}': 0,
        f'{symbol2}': 0,
    }

    pl_series = []
    holding_series = {
        f'{symbol1}': [],
        f'{symbol2}': [],
    }
    prev_row = None

    for date, row in pd.concat([price1, price2, n_shares1, n_shares2, signal_series], axis=1).iterrows():
        signal = row[signal_series.name]
        holding_series[f'{symbol1}'].append(share_holdings[f'{symbol1}'])
        holding_series[f'{symbol2}'].append(share_holdings[f'{symbol2}'])
        if share_holdings[f'{symbol1}'] != 0 and share_holdings[f'{symbol2}'] != 0 and prev_row[signal_series.name] != 0:

            t1_shares = share_holdings[f'{symbol1}']
            t1_cprice = row[f'{price1.name}']
            t1_pprice = prev_row[f'{price1.name}']
            t1_dprice = t1_cprice - t1_pprice
            t2_shares = share_holdings[f'{symbol2}']
            t2_cprice = row[f'{price2.name}']
            t2_pprice = prev_row[f'{price2.name}']
            t2_dprice = t2_cprice - t2_pprice

            change = t1_shares * t1_dprice + t2_shares * t2_dprice
            current_pos_pl += change
            current_pl += change

            if change <= -trailing_stop * gross_entry_outlay:
                share_holdings[f'{symbol1}'] = 0
                share_holdings[f'{symbol2}'] = 0
                current_pos_pl = 0
                gross_entry_outlay = 0

        pl_series.append(current_pl)

        
        # signal change from 0
        if signal != prev_signal and prev_signal == 0:
            if signal == 1:
                share_holdings[f'{symbol1}'] = 0
                share_holdings[f'{symbol2}'] = 0
                share_holdings[f'{symbol1}'] -= row[n_shares1.name]
                share_holdings[f'{symbol2}'] += row[n_shares2.name]
                gross_entry_outlay = 0
                gross_entry_outlay += row[n_shares1.name] * row[f'{price1.name}']
                gross_entry_outlay += row[n_shares2.name] * row[f'{price2.name}']
                current_pos_pl = 0
            elif signal == -1:
                share_holdings[f'{symbol1}'] = 0
                share_holdings[f'{symbol2}'] = 0
                share_holdings[f'{symbol1}'] += row[n_shares1.name]
                share_holdings[f'{symbol2}'] -= row[n_shares2.name]
                gross_entry_outlay = 0
                gross_entry_outlay += row[n_shares1.name] * row[f'{price1.name}']
                gross_entry_outlay += row[n_shares2.name] * row[f'{price2.name}']
                current_pos_pl = 0
        # flipped position
        elif prev_signal != 0 and signal != 0 and prev_signal != signal:
            if signal == 1:
                share_holdings[f'{symbol1}'] = 0
                share_holdings[f'{symbol2}'] = 0
                share_holdings[f'{symbol1}'] -= row[n_shares1.name]
                share_holdings[f'{symbol2}'] += row[n_shares2.name]
                gross_entry_outlay = 0
                gross_entry_outlay += row[n_shares1.name] * row[f'{price1.name}']
                gross_entry_outlay += row[n_shares2.name] * row[f'{price2.name}']
                current_pos_pl = 0
            elif signal == -1:
                share_holdings[f'{symbol1}'] = 0
                share_holdings[f'{symbol2}'] = 0
                share_holdings[f'{symbol1}'] += row[n_shares1.name]
                share_holdings[f'{symbol2}'] -= row[n_shares2.name]
                gross_entry_outlay = 0
                gross_entry_outlay += row[n_shares1.name] * row[f'{price1.name}']
                gross_entry_outlay += row[n_shares2.name] * row[f'{price2.name}']
                current_pos_pl = 0

        
        elif signal == 0:
            share_holdings[f'{symbol1}'] = 0
            share_holdings[f'{symbol2}'] = 0
            current_pos_pl = 0



        
        prev_row = row
        prev_signal = signal

    pl_series = pd.Series(pl_series, index=signal_series.index, name="PnL")
    holdings_df = pd.DataFrame(holding_series, index=signal_series.index)

