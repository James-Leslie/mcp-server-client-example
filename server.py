# https://modelcontextprotocol.io/docs/develop/build-server
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

# Initialize FastMCP server
mcp = FastMCP("weather")


async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling and proxy support."""
    headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}
    async with httpx.AsyncClient(
        proxy="http://at-proxy.aucklandtransport.govt.nz:8080"
    ) as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return (
        f"Event: {props.get('event', 'Unknown')}\n"
        f"Area: {props.get('areaDesc', 'Unknown')}\n"
        f"Severity: {props.get('severity', 'Unknown')}\n"
        f"Description: {props.get('description', 'No description available')}\n"
        f"Instructions: {props.get('instruction', 'No specific instructions provided')}"
    )


@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a given U.S. state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state.upper()}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)


@mcp.tool()
async def get_forecast(lat: float, lon: float) -> str:
    """Get the weather forecast for given location.

    Args:
        lat: Latitude of the location
        lon: Longitude of the location
    """

    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{lat},{lon}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = (
            f"{period['name']}:\n"
            f"Temperature: {period['temperature']}°{period['temperatureUnit']}\n"
            f"Wind: {period['windSpeed']} {period['windDirection']}\n"
            f"Forecast: {period['detailedForecast']}"
        )
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)


def main():
    # Initialize and run the server
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
