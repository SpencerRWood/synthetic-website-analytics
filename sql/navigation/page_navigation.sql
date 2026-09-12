select
    from_page,
    to_page,
    from_page_name,
    to_page_name,
    transition_count,
    from_page_transition_count,
    observed_transition_probability
from marts.fct_website_page_navigation
order by from_page, to_page;
