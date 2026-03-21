# Awesome ADBC [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> A curated list of resources for ADBC, Apache Arrow's Arrow-native database connectivity standard.

ADBC is a cross-language API and driver ecosystem for database access using Arrow data. This list stays focused on ADBC itself, with a small amount of surrounding context for `dbc`, Flight SQL, and comparisons with older interfaces such as ODBC, JDBC, DB-API, and DBI.

Contributions welcome. Please read the official resource before submitting a summary or new link.

## Contents

- [Official Resources](#official-resources)
- [Getting Started](#getting-started)
- [Official Language APIs](#official-language-apis)
- [Community Bindings](#community-bindings)
- [Drivers](#drivers)
- [Tools and Ecosystem](#tools-and-ecosystem)
- [Comparisons and Context](#comparisons-and-context)
- [Articles and Blog Posts](#articles-and-blog-posts)
- [Talks, Videos, and Audio](#talks-videos-and-audio)
- [News and Tracking](#news-and-tracking)

## Official Resources

- [ADBC Documentation](https://arrow.apache.org/adbc/current/index.html) - The main documentation hub for ADBC.
- [ADBC Specification](https://arrow.apache.org/docs/format/ADBC.html) - The format and API specification.
- [Driver Implementation Status](https://arrow.apache.org/adbc/current/driver/status.html) - Current maturity, packaging, and feature coverage across drivers.
- [Comparison with Other APIs](https://arrow.apache.org/adbc/current/format/comparison.html) - Official mapping between ADBC and APIs such as ODBC, JDBC, DB-API, and Flight SQL.
- [How Drivers and the Driver Manager Work Together](https://arrow.apache.org/adbc/current/format/how_manager.html) - Good background on the driver model.
- [GitHub Repository](https://github.com/apache/arrow-adbc) - Source code, issues, and release artifacts.
- [Introducing ADBC](https://arrow.apache.org/blog/2023/01/05/introducing-arrow-adbc/) - The original Apache Arrow introduction post.
- [Apache Arrow ADBC 22 Release](https://arrow.apache.org/blog/2026/01/09/adbc-22-release/) - Latest release post I found as of March 21, 2026.

## Getting Started

- [C/C++ Quickstart](https://arrow.apache.org/adbc/current/cpp/quickstart.html) - Official first example in C++.
- [Java Quickstart](https://arrow.apache.org/adbc/current/java/quickstart.html) - Official Java getting-started guide.
- [Python Quickstart](https://arrow.apache.org/adbc/current/python/quickstart.html) - Official Python quickstart using SQLite.
- [R Packages Overview](https://arrow.apache.org/adbc/current/r/index.html) - The main entry point for ADBC in R.
- [ADBC Quickstarts](https://github.com/columnar-tech/adbc-quickstarts) - Runnable examples across languages and data systems.

## Official Language APIs

- [C/C++ Overview](https://arrow.apache.org/adbc/current/cpp/index.html) - Main entry point for the C and C++ implementation.
- [C/C++ Driver Manager](https://arrow.apache.org/adbc/current/cpp/driver_manager.html) - Dynamic loading and portability via the driver manager.
- [C/C++ API Reference](https://arrow.apache.org/adbc/current/cpp/api.html) - Low-level reference for the core C/C++ API surface.
- [C#/.NET Packages](https://www.nuget.org/packages/Apache.Arrow.Adbc) - The core ADBC implementation for .NET on NuGet.
- [Go Package Docs](https://pkg.go.dev/github.com/apache/arrow-adbc/go/adbc) - Official Go package documentation for the ADBC interfaces.
- [Go Driver Manager](https://pkg.go.dev/github.com/apache/arrow-adbc/go/adbc/drivermgr) - Go wrapper around the ADBC driver manager.
- [Java Overview](https://arrow.apache.org/adbc/current/java/index.html) - Main Java entry point for quickstart, driver-manager docs, and API reference.
- [Java Driver Manager](https://arrow.apache.org/adbc/current/java/driver_manager.html) - Java driver-manager docs.
- [Python Driver Manager](https://arrow.apache.org/adbc/current/python/driver_manager.html) - The Python driver manager plus DB-API interface.
- [Python Module Index](https://arrow.apache.org/adbc/current/python/index.html) - Python packages, cookbook pages, and API reference.
- [Python Cookbook](https://arrow.apache.org/adbc/current/python/cookbook.html) - Recipes for DB-API, Flight SQL, PostgreSQL, and SQLite.
- [R Packages](https://arrow.apache.org/adbc/current/r/index.html) - `adbcdrivermanager` plus database-specific R packages.
- [Rust Driver Manager](https://arrow.apache.org/adbc/current/rust/driver_manager.html) - Rust driver-manager docs.
- [JDBC Adapter](https://arrow.apache.org/adbc/current/driver/jdbc.html) - ADBC's Java adapter for JDBC-accessible systems.
- [Using ADBC in Java](https://columnar.tech/blog/adbc-java) - Practical Java-focused overview from Columnar.
- [Rust Overview](https://arrow.apache.org/adbc/current/rust/index.html) - Rust APIs, quickstart, and driver-manager docs.

## Community Bindings

- [Elixir `adbc`](https://github.com/elixir-explorer/adbc) - Apache Arrow ADBC bindings for Elixir, maintained in the Explorer ecosystem.

## Drivers

- [BigQuery Driver](https://arrow.apache.org/adbc/current/driver/bigquery.html) - Official BigQuery driver docs.
- [DuckDB Driver](https://arrow.apache.org/adbc/current/driver/duckdb.html) - Official DuckDB driver page from the ADBC docs.
- [Flight SQL Driver](https://arrow.apache.org/adbc/current/driver/flight_sql.html) - Official Flight SQL ADBC driver docs.
- [PostgreSQL Driver](https://arrow.apache.org/adbc/current/driver/postgresql.html) - Official PostgreSQL driver docs.
- [Snowflake Driver](https://arrow.apache.org/adbc/current/driver/snowflake.html) - Official Snowflake driver docs.
- [SQLite Driver](https://arrow.apache.org/adbc/current/driver/sqlite.html) - Official SQLite driver docs.
- [ADBC Driver Foundry Docs](https://docs.adbc-drivers.org/) - Documentation for Foundry-maintained drivers such as BigQuery, Databricks, MySQL, Redshift, Snowflake, SQL Server, and Trino.
- [Writing New Drivers](https://arrow.apache.org/adbc/current/driver/authoring.html) - Official guidance for driver authors.

## Tools and Ecosystem

- [Announcing Columnar](https://columnar.tech/blog/announcing-columnar/) - Company launch post framing the ADBC and driver-distribution problem space.
- [dbc Documentation](https://docs.columnar.tech/dbc/) - The main docs site for `dbc`, the ADBC driver installer and manager.
- [Introducing dbc](https://columnar.tech/blog/introducing-dbc/) - Why `dbc` exists and how it fits into the ADBC workflow.
- [dbc 0.2.0 Announcement](https://columnar.tech/blog/announcing-dbc-0.2.0/) - Recent `dbc` release notes and workflow improvements.
- [dbc Cheatsheet (PDF)](https://docs.columnar.tech/dbc/assets/cheatsheet.pdf) - Quick reference for common `dbc` commands.
- [dbc Driver Manager Concept](https://docs.columnar.tech/dbc/concepts/driver_manager/) - Concise explanation of the ADBC driver-manager model from the `dbc` docs.
- [ADBC Driver Foundry Announcement](https://adbc-drivers.org/2025/10/29/announcing-adbc-driver-foundry.html) - Background on the federated driver-development effort.
- [A Deep Dive into ADBC Driver Optimization](https://columnar.tech/blog/adbc-driver-optimization-deep-dive/) - Performance engineering write-up covering BigQuery, SQL Server, MySQL, and Trino drivers.

## Comparisons and Context

- [DuckDB ADBC: Zero-Copy Data Transfer via Arrow Database Connectivity](https://duckdb.org/2023/08/04/adbc) - Strong technical argument for ADBC with an ADBC-vs-ODBC benchmark.
- [DuckDB ADBC Client Docs](https://duckdb.org/docs/stable/clients/adbc) - DuckDB's own ADBC documentation.
- [Configure ADBC or ODBC Driver for Power BI (Azure Databricks)](https://learn.microsoft.com/en-us/azure/databricks/partners/bi/power-bi-adbc) - Practical comparison of ADBC and ODBC in a production BI workflow.
- [Dremio Power BI Connector Announcement](https://www.dremio.com/blog/announcing-arrow-database-connectivity-adbc-in-microsoft-power-bis-connector-for-dremio/) - Vendor adoption and positioning around ADBC in Power BI.
- [Arrow Flight SQL Spec](https://arrow.apache.org/docs/format/FlightSql.html) - Useful for understanding where Flight SQL complements ADBC rather than replacing it.
- [Arrow C Data Interface](https://arrow.apache.org/docs/13.0/format/CDataInterface.html) - Background on the Arrow interchange layer that underpins a lot of the performance story.
- [PEP 249: Python DB-API 2.0](https://peps.python.org/pep-0249/) - The Python standard that ADBC's Python layer integrates with.
- [R DBI](https://dbi.r-dbi.org/) - The R database interface standard that ADBC integrates with in R.
- [JDBC Overview](https://docs.oracle.com/javase/8/docs/technotes/guides/jdbc/) - Reference point for the legacy Java standard ADBC is often compared with.

## Articles and Blog Posts

- [Arrow Database Connectivity (ADBC) Support for Snowflake](https://medium.com/snowflake/arrow-database-connectivity-adbc-support-for-snowflake-7bfb3a2d9074) - Early Snowflake write-up on the ADBC driver and cross-language use cases.
- [A Quick Start Guide to the Snowflake ADBC Driver with Python](https://medium.com/snowflake/a-quick-start-guide-to-the-snowflake-adbc-driver-with-python-6de3eb28ee52) - Short practical guide to installing and using the Snowflake driver from Python.
- [Achieving 100,000+ Rows/Second Data Processing with R x Snowflake x ADBC](https://medium.com/snowflake-engineering/achieving-100-000-rows-second-data-processing-with-r-snowflake-adbc-apache-arrow-columnar-format-bba28488b271) - Community performance-oriented write-up for R and Snowflake workflows.
- [ADBC: The Future of Database Connectivity](https://medium.com/%40thibaut_gourdel/adbc-the-future-of-database-connectivity-4784c03637e8) - Short external explainer comparing ADBC with ODBC and JDBC.
- [What Is Apache Arrow Flight, Flight SQL, and ADBC?](https://dipankar-tnt.medium.com/what-is-apache-arrow-flight-flight-sql-adbc-a076511122ac) - Introductory article positioning ADBC relative to Flight and Flight SQL.

## Talks, Videos, and Audio

- [Making Moves with Arrow Data: Introducing Arrow Database Connectivity (ADBC)](https://www.datacouncil.ai/talks25/making-moves-with-arrow-data-introducing-arrow-database-connectivity-adbc) - Data Council talk page for Matthew Topol's ADBC introduction.
- [Where We're Going, We Don't Need Rows: Columnar Data Connectivity with ADBC](https://db.cs.cmu.edu/events/futuredata-where-were-going-we-dont-need-rows-columnar-data-connectivity-with-adbc/) - CMU Database Group seminar by Ian Cook.
- [Where We're Going, We Don't Need Rows (YouTube)](https://www.youtube.com/watch?v=TjlmNGNx77E) - Direct video link for Ian Cook's CMU talk.
- [ODBC Takes an Arrow to the Knee](https://fosdem.org/2025/schedule/event/fosdem-2025-4803-odbc-takes-an-arrow-to-the-knee/) - FOSDEM 2025 talk by Matthew Topol.
- [ODBC Takes an Arrow to the Knee: ADBC](https://www.dremio.com/subsurface/on-demand/odbc-takes-an-arrow-to-the-knee-adbc/) - Dremio Subsurface session page for the same talk.
- [From ODBC to ADBC: Modernizing the Data Stack for AI and Analytics](https://podcasts.apple.com/tr/podcast/the-joe-reis-show/id1676305617) - The Joe Reis Show episode with Ian Cook.
- [Ian Cook on YouTube: From ODBC to ADBC](https://www.youtube.com/watch?v=j75BIlqzhUk&t=777s) - Video version of the Joe Reis Show conversation.
- [Machine Learning with ADBC, DuckDB, and XGBoost](https://www.youtube.com/watch?v=J6CawwGwdyk) - Hands-on walkthrough showing an Arrow-native ML pipeline.
- [Training XGBoost on DuckLake Data with ADBC](https://thefulldatastack.substack.com/p/training-xgboost-ducklake-adbc) - Companion article for the DuckLake, DuckDB, and XGBoost workflow.
- [IO + SQL + ADBC Drivers](https://www.youtube.com/watch?v=ZL9n1nrVUcQ&t=6s) - Talk by Will Ayd showing practical SQL and type-safety-oriented driver usage.

## News and Tracking

- [Columnar Current](https://columnar.tech/current/) - Rolling feed of ADBC-related talks, posts, releases, and ecosystem news.
- [Apache Arrow Blog](https://arrow.apache.org/blog/) - Release posts and broader Arrow project news.
