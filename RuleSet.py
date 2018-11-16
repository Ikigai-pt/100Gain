rules = [
# expiration_days < 5 AND current_inventory > 20
{ "conditions": { "all": [
      { "name": "current_inventory",
        "operator": "greater_than",
        "value": 10,
      },
  ]},
  "actions": [
      { "name": "put_on_sale",
        "params": {"sale_percentage": 0.25},
      },
  ],
}]
