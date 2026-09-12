select
    date_day,

    session_count,
    visitor_count,
    event_count,
    page_view_count,

    product_view_count,
    add_to_cart_count,
    begin_checkout_count,
    purchase_count,

    paid_search_session_count,
    display_session_count,
    unattributed_session_count,

    product_view_session_count,
    add_to_cart_session_count,
    begin_checkout_session_count,
    purchase_session_count,

    order_count,
    total_order_value,
    total_items_purchased,

    product_view_session_count::numeric
        / nullif(session_count, 0)
        as session_to_product_view_rate,

    add_to_cart_session_count::numeric
        / nullif(product_view_session_count, 0)
        as product_view_to_cart_rate,

    begin_checkout_session_count::numeric
        / nullif(add_to_cart_session_count, 0)
        as cart_to_checkout_rate,

    purchase_session_count::numeric
        / nullif(begin_checkout_session_count, 0)
        as checkout_to_purchase_rate,

    purchase_session_count::numeric
        / nullif(session_count, 0)
        as session_conversion_rate,

    total_order_value::numeric
        / nullif(order_count, 0)
        as average_order_value,

    total_order_value::numeric
        / nullif(session_count, 0)
        as revenue_per_session

from marts.fct_website_daily_metrics
order by date_day;
