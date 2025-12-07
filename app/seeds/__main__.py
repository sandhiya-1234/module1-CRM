from app.seeds import seed_products, seed_finance

if __name__ == "__main__":
    print("🚀 Running all seed scripts...")
    seed_products.run()
    seed_finance.run()
    print("🎉 All seed data inserted successfully!")
