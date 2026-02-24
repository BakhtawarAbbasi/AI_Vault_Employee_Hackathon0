#!/usr/bin/env python3
"""
Odoo MCP Server
Provides integration with Odoo Community Edition via JSON-RPC
"""

import os
import sys
import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
import xmlrpc.client

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class OdooMCPServer:
    """MCP Server for Odoo integration"""

    def __init__(self):
        """Initialize Odoo connection"""
        self.url = os.getenv('ODOO_URL', 'http://localhost:8069')
        self.db = os.getenv('ODOO_DB', 'odoo')
        self.username = os.getenv('ODOO_USERNAME')
        self.password = os.getenv('ODOO_PASSWORD')

        if not self.username or not self.password:
            logger.warning("ODOO_USERNAME and ODOO_PASSWORD not set")

        self.uid = None
        self.models = None

    def authenticate(self) -> bool:
        """Authenticate with Odoo"""
        try:
            common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
            self.uid = common.authenticate(self.db, self.username, self.password, {})

            if self.uid:
                self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')
                logger.info(f"Authenticated with Odoo as user ID: {self.uid}")
                return True
            else:
                logger.error("Authentication failed")
                return False

        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return False

    def create_invoice(self, partner_name: str, amount: float, description: str,
                      invoice_type: str = 'out_invoice') -> Dict[str, Any]:
        """
        Create an invoice in Odoo

        Args:
            partner_name: Customer/Vendor name
            amount: Invoice amount
            description: Invoice description
            invoice_type: 'out_invoice' (customer) or 'in_invoice' (vendor)

        Returns:
            Dict with success status and invoice details
        """
        try:
            if not self.uid:
                if not self.authenticate():
                    return {"error": "Authentication failed"}

            # Search for partner
            partner_ids = self.models.execute_kw(
                self.db, self.uid, self.password,
                'res.partner', 'search',
                [[['name', '=', partner_name]]]
            )

            if not partner_ids:
                return {"error": f"Partner '{partner_name}' not found"}

            partner_id = partner_ids[0]

            # Create invoice
            invoice_data = {
                'partner_id': partner_id,
                'move_type': invoice_type,
                'invoice_date': datetime.now().strftime('%Y-%m-%d'),
                'invoice_line_ids': [(0, 0, {
                    'name': description,
                    'quantity': 1,
                    'price_unit': amount,
                })]
            }

            invoice_id = self.models.execute_kw(
                self.db, self.uid, self.password,
                'account.move', 'create',
                [invoice_data]
            )

            # Log to business log
            self._log_business_activity(
                f"Created invoice #{invoice_id} for {partner_name}: ${amount}"
            )

            logger.info(f"Created invoice #{invoice_id}")

            return {
                "success": True,
                "invoice_id": invoice_id,
                "partner": partner_name,
                "amount": amount,
                "type": invoice_type,
                "description": description
            }

        except Exception as e:
            logger.error(f"Error creating invoice: {e}")
            self._log_error(f"Failed to create invoice: {e}")
            return {"error": str(e)}

    def list_invoices(self, limit: int = 10, invoice_type: Optional[str] = None) -> Dict[str, Any]:
        """
        List invoices from Odoo

        Args:
            limit: Maximum number of invoices to return
            invoice_type: Filter by type ('out_invoice', 'in_invoice', or None for all)

        Returns:
            Dict with success status and invoice list
        """
        try:
            if not self.uid:
                if not self.authenticate():
                    return {"error": "Authentication failed"}

            # Build search domain
            domain = []
            if invoice_type:
                domain.append(['move_type', '=', invoice_type])

            # Search invoices
            invoice_ids = self.models.execute_kw(
                self.db, self.uid, self.password,
                'account.move', 'search',
                [domain],
                {'limit': limit, 'order': 'id desc'}
            )

            if not invoice_ids:
                return {
                    "success": True,
                    "invoices": [],
                    "count": 0
                }

            # Read invoice details
            invoices = self.models.execute_kw(
                self.db, self.uid, self.password,
                'account.move', 'read',
                [invoice_ids],
                {'fields': ['name', 'partner_id', 'amount_total', 'state',
                           'invoice_date', 'move_type']}
            )

            # Format results
            formatted_invoices = []
            for inv in invoices:
                formatted_invoices.append({
                    'id': inv['id'],
                    'number': inv['name'],
                    'partner': inv['partner_id'][1] if inv['partner_id'] else 'Unknown',
                    'amount': inv['amount_total'],
                    'state': inv['state'],
                    'date': inv['invoice_date'],
                    'type': inv['move_type']
                })

            logger.info(f"Retrieved {len(formatted_invoices)} invoices")

            return {
                "success": True,
                "invoices": formatted_invoices,
                "count": len(formatted_invoices)
            }

        except Exception as e:
            logger.error(f"Error listing invoices: {e}")
            self._log_error(f"Failed to list invoices: {e}")
            return {"error": str(e)}

    def record_payment(self, invoice_id: int, amount: float,
                      payment_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Record a payment for an invoice

        Args:
            invoice_id: Odoo invoice ID
            amount: Payment amount
            payment_date: Payment date (YYYY-MM-DD), defaults to today

        Returns:
            Dict with success status and payment details
        """
        try:
            if not self.uid:
                if not self.authenticate():
                    return {"error": "Authentication failed"}

            if not payment_date:
                payment_date = datetime.now().strftime('%Y-%m-%d')

            # Get invoice details
            invoice = self.models.execute_kw(
                self.db, self.uid, self.password,
                'account.move', 'read',
                [invoice_id],
                {'fields': ['name', 'partner_id', 'amount_total', 'state']}
            )

            if not invoice:
                return {"error": f"Invoice #{invoice_id} not found"}

            invoice = invoice[0]

            # Create payment
            payment_data = {
                'payment_type': 'inbound',
                'partner_id': invoice['partner_id'][0],
                'amount': amount,
                'date': payment_date,
                'ref': f"Payment for {invoice['name']}",
            }

            payment_id = self.models.execute_kw(
                self.db, self.uid, self.password,
                'account.payment', 'create',
                [payment_data]
            )

            # Post the payment
            self.models.execute_kw(
                self.db, self.uid, self.password,
                'account.payment', 'action_post',
                [[payment_id]]
            )

            # Log to business log
            self._log_business_activity(
                f"Recorded payment of ${amount} for invoice {invoice['name']}"
            )

            logger.info(f"Recorded payment #{payment_id} for invoice #{invoice_id}")

            return {
                "success": True,
                "payment_id": payment_id,
                "invoice_id": invoice_id,
                "invoice_number": invoice['name'],
                "amount": amount,
                "date": payment_date
            }

        except Exception as e:
            logger.error(f"Error recording payment: {e}")
            self._log_error(f"Failed to record payment: {e}")
            return {"error": str(e)}

    def _log_business_activity(self, message: str):
        """Log activity to business log"""
        try:
            log_dir = os.path.join(os.path.dirname(__file__), '..', '..',
                                   'AI_Employee_Vault', 'Logs')
            os.makedirs(log_dir, exist_ok=True)

            log_file = os.path.join(log_dir, 'business.log')
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] ODOO: {message}\n")

        except Exception as e:
            logger.error(f"Failed to log business activity: {e}")

    def _log_error(self, message: str):
        """Log error to error log"""
        try:
            log_dir = os.path.join(os.path.dirname(__file__), '..', '..',
                                   'AI_Employee_Vault', 'Logs')
            os.makedirs(log_dir, exist_ok=True)

            log_file = os.path.join(log_dir, 'error.log')
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] ODOO_ERROR: {message}\n")

        except Exception as e:
            logger.error(f"Failed to log error: {e}")

    def handle_request(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP request"""
        try:
            if action == 'create_invoice':
                return self.create_invoice(
                    partner_name=params.get('partner_name'),
                    amount=params.get('amount'),
                    description=params.get('description'),
                    invoice_type=params.get('invoice_type', 'out_invoice')
                )

            elif action == 'list_invoices':
                return self.list_invoices(
                    limit=params.get('limit', 10),
                    invoice_type=params.get('invoice_type')
                )

            elif action == 'record_payment':
                return self.record_payment(
                    invoice_id=params.get('invoice_id'),
                    amount=params.get('amount'),
                    payment_date=params.get('payment_date')
                )

            else:
                return {"error": f"Unknown action: {action}"}

        except Exception as e:
            logger.error(f"Error handling request: {e}")
            return {"error": str(e)}


def main():
    """Main entry point for MCP server"""
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python server.py <action> [params_json]"}))
        sys.exit(1)

    action = sys.argv[1]
    params = {}

    if len(sys.argv) > 2:
        try:
            params = json.loads(sys.argv[2])
        except json.JSONDecodeError:
            print(json.dumps({"error": "Invalid JSON parameters"}))
            sys.exit(1)

    server = OdooMCPServer()
    result = server.handle_request(action, params)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
