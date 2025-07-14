from notion_client import Client

# Initialize your client
notion = Client(auth="YOUR_NOTION_INTEGRATION_TOKEN")

# 1. Create the root “Trading HQ” page
trading_hq = notion.pages.create(
    parent={"type": "workspace", "workspace": True},
    properties={
        "title": [
            {
                "type": "text",
                "text": { "content": "📊 Trading HQ" }
            }
        ]
    }
)
trading_hq_id = trading_hq["id"]


# 2. Create Scalp Trades Database
scalp_db = notion.databases.create(
    parent={"type": "page_id", "page_id": trading_hq_id},
    title=[{"type":"text","text":{"content":"Scalp Trades"}}],
    properties={
        "Date":       {"date": {}},
        "Coin":       {"select": {"options":[{"name":"BTC"},{"name":"ETH"},{"name":"XRP"}]}},
        "Timeframe":  {"select": {"options":[{"name":"1m"},{"name":"3m"},{"name":"5m"}]}},
        "Strategy":   {"select": {"options":[{"name":"Breakout"},{"name":"Pullback"},{"name":"Reversal"}]}},
        "Entry":      {"number": {"format":"number"}},
        "Stop Loss":  {"number": {"format":"number"}},
        "Target 1":   {"number": {"format":"number"}},
        "Target 2":   {"number": {"format":"number"}},
        "Position Size": {"number": {"format":"number"}},
        "Risk %":     {"formula": {"expression":"prop(\"Position Size\")/100"}},
        "Exit":       {"number": {"format":"number"}},
        "Outcome":    {"select": {"options":[{"name":"Win"},{"name":"Loss"},{"name":"Break-Even"}]}},
        "PnL ($)":    {"formula": {"expression":"(prop(\"Exit\")-prop(\"Entry\"))*prop(\"Position Size\")"}},
        "Screenshots":{"files": {}},
        "Notes":      {"rich_text": {}},
        "Lessons":    {"rich_text": {}}
    }
)
scalp_db_id = scalp_db["id"]


# 3. Create Day Trades Database
day_db = notion.databases.create(
    parent={"type": "page_id", "page_id": trading_hq_id},
    title=[{"type":"text","text":{"content":"Day Trades"}}],
    properties={
        "Date":            {"date": {}},
        "Market Bias":     {"select": {"options":[{"name":"Bullish"},{"name":"Bearish"},{"name":"Neutral"}]}},
        "Watchlist":       {"multi_select": {}},
        "Strategy":        {"select": {"options":[{"name":"Breakout"},{"name":"Trend"},{"name":"Range"}]}},
        "Entry":           {"number": {"format":"number"}},
        "Stop Loss":       {"number": {"format":"number"}},
        "TP1":             {"number": {"format":"number"}},
        "TP2":             {"number": {"format":"number"}},
        "Size (Units)":    {"number": {"format":"number"}},
        "Size ($)":        {"formula": {"expression":"prop(\"Size (Units)\") * prop(\"Entry\")"}},
        "Management Notes":{"rich_text": {}},
        "Exit":            {"number": {"format":"number"}},
        "Outcome":         {"select": {"options":[{"name":"Win"},{"name":"Loss"},{"name":"BE"}]}},
        "PnL ($)":         {"formula": {"expression":"(prop(\"Exit\")-prop(\"Entry\"))*prop(\"Size (Units)\")"}},
        "Reflection":      {"rich_text": {}},
        "Improvements":    {"rich_text": {}}
    }
)
day_db_id = day_db["id"]


# 4. Create Daily Pre-Trade Checklist Database
checklist_db = notion.databases.create(
    parent={"type": "page_id", "page_id": trading_hq_id},
    title=[{"type":"text","text":{"content":"Daily Pre-Trade Checklist"}}],
    properties={
        "Date":        {"date": {}},
        "Market Open": {"date": {}},
        "Bias Check":  {"checkbox": {}},
        "Top 5 Coins": {"multi_select": {}},
        "Key Levels":  {"rich_text": {}},
        "Economic Events": {"rich_text": {}},
        "Risk Setup OK": {"checkbox": {}},
        "Ready":       {"checkbox": {}}
    }
)
checklist_db_id = checklist_db["id"]


# 5. Create Weekly Review Database
weekly_db = notion.databases.create(
    parent={"type": "page_id", "page_id": trading_hq_id},
    title=[{"type":"text","text":{"content":"Weekly Review"}}],
    properties={
        "Week Of":       {"date": {}},
        "Total Trades":  {"formula": {"expression":"length(prop(\"Trades\"))"}},
        "Win Rate":      {"number": {"format":"percent"}},
        "Avg R":         {"number": {"format":"number"}},
        "Key Wins":      {"rich_text": {}},
        "Key Losses":    {"rich_text": {}},
        "Adjustments":   {"rich_text": {}},
        "Trades":        {"relation": {"database_id": scalp_db_id}}
    }
)
weekly_db_id = weekly_db["id"]


# 6. Create Monthly Metrics Database
monthly_db = notion.databases.create(
    parent={"type": "page_id", "page_id": trading_hq_id},
    title=[{"type":"text","text":{"content":"Monthly Metrics"}}],
    properties={
        "Month":         {"date": {}},
        "Total PnL":     {"rollup": {"relation_property_name":"Outcome","rollup_property_name":"PnL ($)","function":"sum"}},
        "Monthly Win %": {"rollup": {"relation_property_name":"Outcome","rollup_property_name":"Outcome","function":"percent_true"}},
        "Avg Trade R":   {"formula": {"expression":"prop(\"Total PnL\")/prop(\"Total Trades\")"}},
        "Notes":         {"rich_text": {}},
        "Total Trades":  {"rollup": {"relation_property_name":"Outcome","rollup_property_name":"Outcome","function":"count"}}
    }
)
monthly_db_id = monthly_db["id"]

print("Trading HQ page:", trading_hq_id)
print("Scalp DB:", scalp_db_id)
print("Day DB:", day_db_id)
print("Checklist DB:", checklist_db_id)
print("Weekly DB:", weekly_db_id)
print("Monthly DB:", monthly_db_id)
