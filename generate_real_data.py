import sys
import random
from datetime import datetime, timedelta

sys.path.append(r"C:\Program Files\Odoo 18.0.20241229\server")
import odoo

odoo.tools.config.parse_config(['-c', r'C:\Users\Arilano\Downloads\Project ARICE\Project Odoo\odoo.conf'])
registry = odoo.registry('Business_Intelegent_Project')

COMPANIES = [
    "PT Indofood CBP Sukses Makmur Tbk", "PT Unilever Indonesia Tbk", 
    "PT Telekomunikasi Selular (Telkomsel)", "PT Astra International Tbk", 
    "PT Bank Central Asia Tbk", "PT Pertamina (Persero)", 
    "PT Garuda Indonesia (Persero) Tbk", "PT GoTo Gojek Tokopedia Tbk", 
    "PT Sumber Alfaria Trijaya Tbk (Alfamart)", "PT Indomarco Prismatama (Indomaret)",
    "PT Mayora Indah Tbk", "PT Kalbe Farma Tbk", "PT Gudang Garam Tbk",
    "PT HM Sampoerna Tbk", "PT Telkom Indonesia (Persero) Tbk",
    "PT Bank Mandiri (Persero) Tbk", "PT Bank Rakyat Indonesia (Persero) Tbk",
    "PT United Tractors Tbk", "PT Adaro Energy Indonesia Tbk", "PT Charoen Pokphand Indonesia Tbk"
]

PRODUCTS = [
    ("Indomie Goreng Special", 3000, 2500),
    ("Aqua Air Mineral 600ml", 3500, 2000),
    ("Chitato Sapi Panggang 68g", 12500, 9000),
    ("Teh Pucuk Harum 350ml", 4000, 3000),
    ("Tolak Angin Cair Sachet", 3500, 2500),
    ("Pepsodent Pasta Gigi 190g", 15000, 11000),
    ("Lifebuoy Sabun Cair 450ml", 25000, 18000),
    ("Sunlight Jeruk Nipis 755ml", 18000, 14000),
    ("Rinso Anti Noda 700g", 22000, 17000),
    ("Dancow Fortigro Full Cream 800g", 95000, 80000),
    ("Susu Bear Brand 189ml", 10000, 8500),
    ("Sari Roti Roti Tawar Spesial", 17000, 13000),
    ("SilverQueen Milk Chocolate 62g", 16000, 12000),
    ("Ultra Milk Cokelat 1L", 19000, 15000),
    ("Minyak Goreng Bimoli 2L", 38000, 32000),
    ("Kopi Kapal Api Special Mix", 15000, 11000),
    ("Bango Kecap Manis 520ml", 24000, 19000),
    ("Taro Net Seaweed 65g", 8000, 6000),
    ("Beng-Beng Chocolate", 3000, 2000),
    ("Yakult Minuman Susu Fermentasi", 10000, 8000)
]

def generate_real_mock_data():
    with registry.cursor() as cr:
        env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
        print("Memulai pembuatan data dummy nyata...")
        
        # 1. Ensure Partners
        partners = []
        for cname in COMPANIES:
            partner = env['res.partner'].search([('name', '=', cname)], limit=1)
            if not partner:
                partner = env['res.partner'].create({'name': cname, 'is_company': True})
            partners.append(partner)

        # 2. Ensure Products
        products = []
        for pname, price, cost in PRODUCTS:
            product = env['product.product'].search([('name', '=', pname)], limit=1)
            if not product:
                product = env['product.product'].create({
                    'name': pname, 
                    'type': 'consu', 
                    'list_price': price,
                    'standard_price': cost,
                })
            products.append(product)

        end_date = datetime.now()
        start_date = end_date - timedelta(days=180)

        def random_date():
            return start_date + timedelta(days=random.randint(0, 180))

        # 3. CRM Leads (40-60)
        num_crm = random.randint(40, 60)
        print(f"Membuat {num_crm} Real CRM Leads...")
        for i in range(num_crm):
            r_date = random_date()
            lead = env['crm.lead'].create({
                'name': f'Pengadaan Rutin {random_date().strftime("%b %Y")}',
                'partner_id': random.choice(partners).id,
                'expected_revenue': random.randint(10, 500) * 1000000,
                'probability': random.randint(10, 100),
                'create_date': r_date.strftime('%Y-%m-%d %H:%M:%S'),
            })
            if random.random() > 0.5:
                lead.action_set_won()
            elif random.random() > 0.8:
                lead.action_set_lost()

        # 4. Sales Orders (40-60)
        num_sales = random.randint(40, 60)
        print(f"Membuat {num_sales} Real Sales Orders...")
        for i in range(num_sales):
            r_date = random_date()
            so = env['sale.order'].create({
                'partner_id': random.choice(partners).id,
                'date_order': r_date.strftime('%Y-%m-%d %H:%M:%S'),
            })
            for j in range(random.randint(2, 6)):
                env['sale.order.line'].create({
                    'order_id': so.id,
                    'product_id': random.choice(products).id,
                    'product_uom_qty': random.randint(50, 1000),
                })
            if random.random() > 0.3:
                so.action_confirm()

        # 5. Purchase Orders (40-60)
        num_po = random.randint(40, 60)
        print(f"Membuat {num_po} Real Purchase Orders...")
        for i in range(num_po):
            r_date = random_date()
            po = env['purchase.order'].create({
                'partner_id': random.choice(partners).id,
                'date_order': r_date.strftime('%Y-%m-%d %H:%M:%S'),
            })
            for j in range(random.randint(2, 6)):
                env['purchase.order.line'].create({
                    'order_id': po.id,
                    'product_id': random.choice(products).id,
                    'product_qty': random.randint(100, 5000),
                    'price_unit': random.choice(products).standard_price,
                })
            if random.random() > 0.4:
                po.button_confirm()

        # 6. Invoices (40-60)
        num_inv = random.randint(40, 60)
        print(f"Membuat {num_inv} Real Invoices/Bills...")
        for i in range(num_inv):
            r_date = random_date()
            inv_type = random.choice(['out_invoice', 'in_invoice'])
            inv = env['account.move'].create({
                'move_type': inv_type,
                'partner_id': random.choice(partners).id,
                'invoice_date': r_date.strftime('%Y-%m-%d'),
            })
            for j in range(random.randint(1, 5)):
                env['account.move.line'].create({
                    'move_id': inv.id,
                    'product_id': random.choice(products).id,
                    'quantity': random.randint(10, 500),
                    'price_unit': random.choice(products).list_price if inv_type == 'out_invoice' else random.choice(products).standard_price,
                })
            if random.random() > 0.2:
                try:
                    inv.action_post()
                except Exception as e:
                    pass

        # COMMIT is required!
        print("Menyimpan ke database...")
        cr.commit()
        print("Selesai membuat semua data nyata!")

if __name__ == '__main__':
    generate_real_mock_data()
