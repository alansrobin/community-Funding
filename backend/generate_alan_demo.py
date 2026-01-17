"""
Generate demo automated reminder email for Alan S Robin
"""
from app.notifications import notification_engine
from app.intelligence import IntelligenceEngine

# Member data for Alan S Robin
member_name = "Alan S Robin"
classification = "High-risk Delay"  # Let's make it more interesting
priority = "Early Reminder"

# Generate an adaptive message using the intelligence engine
# Simulating a high-risk member scenario
message = """Dear Alan,

We noticed your consistent support to our community, and we're reaching out early to give you extra time to plan for your upcoming contribution.

Your timely participation helps us maintain our community programs and support those in need. We understand life can get busy, which is why we're giving you advance notice.

Thank you for being a valued member of our community. Your contributions make a real difference!"""

# Generate the enhanced email with statistics
html_email = notification_engine.generate_email_with_stats(
    member_name="Alan S Robin",
    message=message,
    monthly_amount=1500,  # ₹1500 monthly contribution
    due_date="2026-02-01",  # Due on Feb 1st
    total_contributions=12,  # Been a member for a year
    paid_count=8,  # Paid 8 out of 12
    missed_count=4,  # 4 pending
    classification="High-risk Delay"  # High-risk classification
)

# Save to file
output_file = "demo_email_alan_s_robin.html"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html_email)

print("=" * 60)
print("✅ DEMO EMAIL GENERATED FOR ALAN S ROBIN")
print("=" * 60)
print(f"\n📧 Email saved to: {output_file}")
print(f"\n📊 Member Statistics:")
print(f"   Name: Alan S Robin")
print(f"   Classification: High-risk Delay (RED badge)")
print(f"   Priority: ⚡ EARLY REMINDER (7 days before)")
print(f"   Total Contributions: 12")
print(f"   Paid: 8 (66.7%)")
print(f"   Pending: 4 (33.3%)")
print(f"   Monthly Amount: ₹1,500")
print(f"   Due Date: February 1, 2026")
print(f"\n🎨 Visual Elements:")
print(f"   • 3 Statistics Cards")
print(f"   • Green progress bar at 66.7%")
print(f"   • Red progress bar at 33.3%")
print(f"   • RED classification badge")
print(f"   • Yellow highlighted due date box")
print(f"\n👀 Open '{output_file}' in your browser to see it!")
print("=" * 60)
