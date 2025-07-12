import json
from selenium.webdriver.remote.webdriver import WebDriver


def mark_test_status(driver: WebDriver, status: str, reason: str = "") -> None:
    """
    Marks the status of the BrowserStack session.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        status (str): "passed" or "failed"
        reason (str): Reason for the test result.
    """
    if status not in {"passed", "failed"}:
        raise ValueError("Status must be 'passed' or 'failed'.")

    payload = {
        "action": "setSessionStatus",
        "arguments": {
            "status": status,
            "reason": reason or f"Test marked as {status}."
        }
    }

    try:
        # Convert dict to JSON string before sending to BrowserStack
        driver.execute_script(f'browserstack_executor: {json.dumps(payload)}')
    except Exception as e:
        print(f"⚠️ Failed to mark status on BrowserStack: {e}")
