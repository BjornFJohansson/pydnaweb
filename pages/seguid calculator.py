import streamlit as st
import streamlit.components.v1 as components


components.html(
    """
    <!doctype html>
    <html lang="en">

    <head>
        <link rel="icon" type="image/png" href="/favicon.png"/>
        <link rel="icon" type="image/png" href="https://example.com/favicon.png"/>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">

        <script src="https://rawcdn.githack.com/seguid/seguid-javascript/0.2.0/seguid.js"></script>
        <script src="https://rawcdn.githack.com/seguid/seguid-calculator/0.1.0/seguid-calculator.js"></script>

        <title>SEGUID v2 Calculator</title>
    </head>

    <body>
        <div id="seguid-calculator"></div>

        <script>
           seguid_calulator();
        </script>
      </body>
    </html>
    """,
    height = 1000,
    width=800,
)
