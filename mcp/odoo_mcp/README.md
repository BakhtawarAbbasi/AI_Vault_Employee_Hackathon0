# Odoo MCP Server

## Overview

MCP Server for integrating with Odoo Community Edition via XML-RPC (JSON-RPC compatible).

## Features

- **Create Invoice**: Create customer or vendor invoices
- **List Invoices**: Retrieve and filter invoices
- **Record Payment**: Record payments against invoices

## Installation

### Prerequisites

```bash
# Install required Python package
pip install xmlrpc
```

### Environment Variables

Set the following environment variables:

```bash
export ODOO_URL="http://localhost:8069"
export ODOO_DB="odoo"
export ODOO_USERNAME="admin"
export ODOO_PASSWORD="your-password"
```

## Usage

### Create Invoice

```bash
python mcp/odoo_mcp/server.py create_invoice '{
  "partner_name": "Customer Name",
  "amount": 1000.00,
  "description": "Consulting services",
  "invoice_type": "out_invoice"
}'
```

**Response:**
```json
{
  "success": true,
  "invoice_id": 123,
  "partner": "Customer Name",
  "amount": 1000.00,
  "type": "out_invoice",
  "description": "Consulting services"
}
```

### List Invoices

```bash
# List all invoices (default limit: 10)
python mcp/odoo_mcp/server.py list_invoices '{}'

# List customer invoices only
python mcp/odoo_mcp/server.py list_invoices '{
  "invoice_type": "out_invoice",
  "limit": 20
}'
```

**Response:**
```json
{
  "success": true,
  "invoices": [
    {
      "id": 123,
      "number": "INV/2026/0001",
      "partner": "Customer Name",
      "amount": 1000.00,
      "state": "posted",
      "date": "2026-02-24",
      "type": "out_invoice"
    }
  ],
  "count": 1
}
```

### Record Payment

```bash
python mcp/odoo_mcp/server.py record_payment '{
  "invoice_id": 123,
  "amount": 1000.00,
  "payment_date": "2026-02-24"
}'
```

**Response:**
```json
{
  "success": true,
  "payment_id": 456,
  "invoice_id": 123,
  "invoice_number": "INV/2026/0001",
  "amount": 1000.00,
  "date": "2026-02-24"
}
```

## Integration with AI Employee

### Automatic Logging

All Odoo operations are automatically logged to:
- `AI_Employee_Vault/Logs/business.log` - Successful operations
- `AI_Employee_Vault/Logs/error.log` - Errors and failures

### Scheduler Integration

Add to `scripts/scheduler.py`:

```python
# Sync Odoo invoices daily
scheduler.add_task(
    name="odoo_sync",
    interval_seconds=86400,  # Daily
    command="mcp/odoo_mcp/server.py",
    args=["list_invoices", '{"limit": 50}']
)
```

## Error Handling

The server includes comprehensive error handling:
- Authentication failures
- Partner not found
- Invoice not found
- Network errors
- Invalid parameters

All errors are logged and returned in a consistent format:

```json
{
  "error": "Error message description"
}
```

## Security

- Credentials stored in environment variables
- No hardcoded passwords
- Secure XML-RPC communication
- Complete audit trail

## Odoo Setup

### Required Odoo Modules

Ensure these modules are installed in your Odoo instance:
- `account` - Accounting module
- `account_payment` - Payment module

### User Permissions

The Odoo user needs the following permissions:
- Accounting: Create/Read invoices
- Accounting: Create/Read payments
- Contacts: Read partners

## Testing

Test the connection:

```bash
# Test authentication
python mcp/odoo_mcp/server.py list_invoices '{}'
```

If successful, you'll see a list of invoices or an empty list.

## Troubleshooting

### Authentication Failed

- Check `ODOO_URL`, `ODOO_DB`, `ODOO_USERNAME`, `ODOO_PASSWORD`
- Verify Odoo is running and accessible
- Check user credentials in Odoo

### Partner Not Found

- Ensure the partner exists in Odoo
- Check exact name spelling (case-sensitive)
- Create the partner in Odoo first

### Invoice Not Found

- Verify the invoice ID exists
- Check if you have permission to access the invoice

## API Reference

### create_invoice(partner_name, amount, description, invoice_type)

Creates a new invoice in Odoo.

**Parameters:**
- `partner_name` (string): Customer/vendor name
- `amount` (float): Invoice amount
- `description` (string): Invoice line description
- `invoice_type` (string): 'out_invoice' or 'in_invoice'

**Returns:** Invoice details or error

### list_invoices(limit, invoice_type)

Lists invoices from Odoo.

**Parameters:**
- `limit` (int): Maximum invoices to return (default: 10)
- `invoice_type` (string, optional): Filter by type

**Returns:** List of invoices or error

### record_payment(invoice_id, amount, payment_date)

Records a payment for an invoice.

**Parameters:**
- `invoice_id` (int): Odoo invoice ID
- `amount` (float): Payment amount
- `payment_date` (string, optional): Date in YYYY-MM-DD format

**Returns:** Payment details or error

## Production Deployment

### Environment Setup

```bash
# Production environment variables
export ODOO_URL="https://your-odoo-instance.com"
export ODOO_DB="production_db"
export ODOO_USERNAME="api_user"
export ODOO_PASSWORD="secure-password"
```

### Logging

Logs are written to:
- `AI_Employee_Vault/Logs/business.log`
- `AI_Employee_Vault/Logs/error.log`

Monitor these files for operational status.

## Support

For issues or questions:
1. Check Odoo server logs
2. Review `AI_Employee_Vault/Logs/error.log`
3. Verify environment variables
4. Test Odoo connection manually

---

**Status:** Production Ready ✅
**Version:** 1.0.0
**Last Updated:** 2026-02-24
