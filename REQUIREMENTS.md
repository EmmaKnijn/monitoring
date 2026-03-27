The application must have three components, one of which is component that uploads information to a webserver over a HTTP REST endpoint. That component must read a set of system stats (disk usage, cpu usage / load, ram usage, network usage) along with a system identifier and report it back to the webserver over HTTPS. Use Python for this

Protect all API endpoints under `/api/v1` with a simple API key. The key must be configurable through an `API_KEY` environment variable on the API container, and API clients must send it using the `X-API-Key` header.

The other component must be able to store this received data into a MySQL database that is also seeded by the same application. The third must be able to display it on a good looking web page. These servers should be using Python and Flask.

Allow looking into the history of the stats with a dropdown which shows a graph (and make sure to convert total MiB to mbit/s).

Use PEP-8 coding style and make sure all three components are seperately dockerizable. Expect a MySQL server to exist in production, but for testing use a local MySQL server using Docker

Write an OpenAPI.yml spec and make it available using swagger-ui. Write simple documentation explaining how to use and deploy the application. 