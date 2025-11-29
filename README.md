# API Testing Framework

A Python-based API testing framework built with **pytest** and **requests**, designed for testing RESTful APIs with a clean, maintainable architecture.

## 📋 Features

- **Separation of Concerns** - API logic is separate from test logic
- **Reusability** - Clients can be reused across multiple tests
- **Maintainability** - Changes to endpoints only need updates in one place
- **Configuration** - Environment variables allow different settings per environment
- **Fixtures** - Shared setup/teardown logic via pytest fixtures

## 📁 Project Structure

```
api-testing/
├── clients/                    # API client classes
│   ├── __init__.py
│   ├── base_client.py          # Base HTTP client with common methods
│   └── products_client.py      # Products API client
├── config/                     # Configuration settings
│   ├── __init__.py
│   └── settings.py             # Environment-based configuration
├── tests/                      # Test suites
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures
│   └── products/               # Products API tests
│       ├── __init__.py
│       ├── test_get_products.py
│       ├── test_post_products.py
│       ├── test_patch_products.py
│       └── test_delete_products.py
├── pytest.ini                  # Pytest configuration
├── requirements.txt            # Python dependencies
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd api-testing
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

The framework uses environment variables for configuration. You can set them directly or create a `.env` file.

| Variable | Default | Description |
|----------|---------|-------------|
| `API_BASE_URL` | `http://127.0.0.1:8000` | Base URL of the API |
| `API_KEY` | (default key) | API authentication key |
| `API_TIMEOUT` | `30` | Request timeout in seconds |

### Setting Environment Variables

```bash
export API_BASE_URL="https://api.example.com"
export API_KEY="your-api-key"
export API_TIMEOUT="60"
```

## 🧪 Running Tests

### Run all tests
```bash
pytest
```

### Run tests with verbose output
```bash
pytest -v
```

### Run specific test file
```bash
pytest tests/products/test_get_products.py
```

### Run specific test class
```bash
pytest tests/products/test_get_products.py::TestGetProducts
```

### Run specific test
```bash
pytest tests/products/test_get_products.py::TestGetProducts::test_get_products_returns_200
```

### Run tests by marker
```bash
# Run smoke tests only
pytest -m smoke

# Run critical tests
pytest -m critical

# Run regression tests
pytest -m regression
```

### Run tests with detailed output
```bash
pytest -v --tb=long
```

## 📊 Allure Reporting

This framework uses **Allure Report** for beautiful, interactive test reports with detailed insights.

### Prerequisites

Install Allure command-line tool:

**macOS:**
```bash
brew install allure
```

**Linux:**
```bash
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure
```

**Windows:**
```bash
scoop install allure
```

Or download from: https://github.com/allure-framework/allure2/releases

### Generate and View Reports

1. **Run tests** (results are saved to `allure-results/`):
   ```bash
   pytest
   ```

2. **Generate HTML report:**
   ```bash
   allure generate allure-results --clean -o allure-report
   ```

3. **Open report in browser:**
   ```bash
   allure open allure-report
   ```

Or use the shortcut to serve the report directly:
```bash
allure serve allure-results
```

### Report Features

- 📈 **Dashboard** - Overview with pass/fail statistics and trends
- 📋 **Test Suites** - Organized by Epic > Feature > Story
- 🔍 **Test Details** - Step-by-step execution with attachments
- 📎 **Attachments** - Request/response payloads in JSON format
- ⏱️ **Timeline** - Visual test execution timeline
- 🏷️ **Categories** - Group failures by type
- 📊 **Graphs** - Severity distribution and duration charts

## 🏗️ Architecture

### Base Client

The `BaseClient` class provides common HTTP methods (GET, POST, PATCH, PUT, DELETE) with:
- Session management
- Default headers (API key, Content-Type)
- Configurable timeout
- URL building

```python
from clients.base_client import BaseClient

class MyApiClient(BaseClient):
    ENDPOINT = "/my-endpoint/"
    
    def get_items(self):
        return self.get(self.ENDPOINT)
```

### API Clients

Specific API clients extend `BaseClient` to provide domain-specific methods:

```python
from clients.products_client import ProductsClient

client = ProductsClient()
response = client.get_products()
response = client.create_product(name="Widget", price=29.99, stock=100)
```

### Fixtures

Pytest fixtures in `conftest.py` provide reusable test setup:

- `products_client` - Session-scoped client instance
- `created_product` - Creates a test product and cleans up after test

## 📝 Writing Tests

### Example Test

```python
import pytest
from clients.products_client import ProductsClient


class TestGetProducts:

    def test_get_products_returns_200(self, products_client: ProductsClient):
        response = products_client.get_products()
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_product_not_found_returns_404(self, products_client: ProductsClient):
        response = products_client.get_product(product_id=999999)
        
        assert response.status_code == 404
```

### Using Fixtures

```python
def test_update_product(self, products_client, created_product):
    if created_product is None:
        pytest.skip("Product creation failed")
    
    response = products_client.update_product(
        product_id=created_product["id"],
        name="Updated Name"
    )
    
    assert response.status_code == 200
```

## 🔧 Adding New API Clients

1. Create a new client file in `clients/`:

```python
# clients/users_client.py
from clients.base_client import BaseClient

class UsersClient(BaseClient):
    ENDPOINT = "/users/"
    
    def get_users(self):
        return self.get(self.ENDPOINT)
    
    def create_user(self, name: str, email: str):
        payload = {"name": name, "email": email}
        return self.post(self.ENDPOINT, data=payload)
```

2. Add fixtures in `conftest.py`:

```python
@pytest.fixture(scope="session")
def users_client():
    client = UsersClient()
    yield client
    client.close()
```

3. Create test files in `tests/users/`:

```python
# tests/users/test_get_users.py
class TestGetUsers:
    def test_get_users_returns_200(self, users_client):
        response = users_client.get_users()
        assert response.status_code == 200
```

## 📦 Dependencies

| Package | Version | Description |
|---------|---------|-------------|
| pytest | 7.4.3 | Testing framework |
| requests | 2.31.0 | HTTP library |
| allure-pytest | 2.15.2 | Allure reporting integration |

## 📄 License

This project is licensed under the MIT License.
