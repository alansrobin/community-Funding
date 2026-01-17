"""
Quick test script to generate and save a sample email with statistics
"""
from app.notifications import notification_engine

# Generate sample email
html_email = notification_engine.generate_email_with_stats(
    member_name="John Doe",
    message="This is a friendly reminder about your upcoming monthly contribution. Your support helps our community thrive!",
    monthly_amount=1000,
    due_date="2026-01-25",
    total_contributions=7,
    paid_count=5,
    missed_count=2,
    classification="Regular"
)

# Save to file
output_file = "sample_email_with_stats.html"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html_email)

print(f"✅ Sample email saved to: {output_file}")
print(f"📧 Open this file in your browser to see what members will receive!")
print(f"\nEmail includes:")
print("  • 3 stat cards (Total: 7, Paid: 5, Pending: 2)")
print("  • Visual progress bars (71.4% paid)")
print("  • Classification badge (REGULAR)")
print("  • Due date highlight (₹1000 on Jan 25)")
