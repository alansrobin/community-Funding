from datetime import datetime, timedelta
from typing import List, Dict
import statistics
import random

class IntelligenceEngine:
    """
    Advanced behavior analysis and prediction engine
    """
    
    @staticmethod
    def calculate_risk_score(contributions: List[dict], member: dict) -> float:
        """
        Calculate risk score (0-100) based on payment behavior
        Higher score = higher risk
        """
        if not contributions:
            return 50.0  # Neutral for new members
        
        total = len(contributions)
        paid = sum(1 for c in contributions if c.get("paid_date"))
        missed = total - paid
        
        # Base score from missed payment ratio
        missed_ratio = missed / total
        base_score = missed_ratio * 60
        
        # Add delay penalty
        delays = []
        for c in contributions:
            if c.get("paid_date"):
                due_date = datetime.strptime(c["due_date"], "%Y-%m-%d")
                paid_date = datetime.strptime(c["paid_date"], "%Y-%m-%d")
                delay = (paid_date - due_date).days
                if delay > 0:
                    delays.append(delay)
        
        if delays:
            avg_delay = statistics.mean(delays)
            delay_score = min(avg_delay / 30 * 40, 40)  # Cap at 40
            base_score += delay_score
        
        return min(base_score, 100.0)
    
    @staticmethod
    def predict_delay_likelihood(contributions: List[dict], member: dict) -> Dict:
        """
        Predict if member is likely to delay next payment
        Returns prediction with confidence and estimated delay days
        """
        if len(contributions) < 2:
            return {
                "will_delay": False,
                "confidence": 0.3,
                "estimated_delay_days": 0,
                "factors": ["Insufficient history"]
            }
        
        # Analyze recent pattern (last 3 contributions)
        recent = contributions[-3:]
        recent_delays = []
        paid_delays = []  # Only delays from actually paid contributions
        factors = []
        
        for c in recent:
            if c.get("paid_date"):
                due_date = datetime.strptime(c["due_date"], "%Y-%m-%d")
                paid_date = datetime.strptime(c["paid_date"], "%Y-%m-%d")
                delay = (paid_date - due_date).days
                if delay > 0:
                    recent_delays.append(delay)
                    paid_delays.append(delay)
            else:
                # Unpaid contribution
                due_date = datetime.strptime(c["due_date"], "%Y-%m-%d")
                current_delay = (datetime.now() - due_date).days
                recent_delays.append(max(current_delay, 30))  # Assume ongoing
        
        # Calculate prediction
        if not recent_delays:
            will_delay = False
            confidence = 0.7
            estimated_days = 0
            factors.append("Consistent on-time payments")
        else:
            avg_recent_delay = statistics.mean(recent_delays)
            
            # Use paid delays for prediction if available, otherwise fall back to all delays
            if paid_delays:
                avg_paid_delay = statistics.mean(paid_delays)
                will_delay = avg_paid_delay > 7  # Only predict delay if PAID contributions were late
                estimated_days = int(avg_paid_delay)
            else:
                # No paid history in recent window - check if there are unpaid
                unpaid_count = len(recent) - len(paid_delays)
                will_delay = unpaid_count >= 2  # Predict delay if 2+ recent unpaid
                estimated_days = int(avg_recent_delay)
            
            # More nuanced confidence calculation
            # Base confidence on: consistency of delays + data quality
            paid_ratio = len(paid_delays) / len(recent) if recent else 0
            data_quality = min(len(contributions) / 10, 1.0)  # More history = higher confidence (cap at 10)
            
            # Calculate variance in delays (lower variance = more predictable = higher confidence)
            if len(recent_delays) > 1:
                delay_variance = statistics.stdev(recent_delays)
                consistency_factor = max(0, 1 - (delay_variance / 30))  # Normalize
            else:
                consistency_factor = 0.5
            
            # Combine factors for confidence
            confidence = (paid_ratio * 0.4) + (data_quality * 0.3) + (consistency_factor * 0.3)
            confidence = min(max(confidence, 0.3), 0.95)  # Cap between 30% and 95%
            
            if avg_recent_delay > 15:
                factors.append("Consistently late payments")
            if avg_recent_delay > 30:
                factors.append("Extended delays observed")
            
            # Check trend
            if len(recent_delays) >= 2:
                if recent_delays[-1] > recent_delays[0]:
                    factors.append("Delays are increasing")
                    confidence = min(confidence + 0.1, 0.95)
        
        return {
            "will_delay": will_delay,
            "confidence": round(confidence, 2),
            "estimated_delay_days": estimated_days,
            "factors": factors if factors else ["Limited data"]
        }
    
    @staticmethod
    def generate_adaptive_reminder(member: dict, classification: str, 
                                   prediction: Dict, days_until_due: int) -> str:
        """
        Generate context-aware, ethically nudged reminder message
        Uses psychological frameworks: Social Proof, Loss Aversion, Positive Reinforcement
        """
        name = member["name"]
        amount = member["monthly_amount"]
        
        # 1. POSITIVE REINFORCEMENT (For Regular/Good Members)
        if classification == "Regular" and not prediction.get("will_delay"):
            streak = 5 # Simulated streak data
            templates = [
                (
                    f"Hi {name}, you've been an amazing supporter! 🌟 Thanks to your 5-month streak of timely contributions, "
                    f"we've been able to fund essential community projects. Your upcoming contribution of ₹{amount} due in {days_until_due} days "
                    f"helps keep this momentum going. Thank you for being a pillar of our community!"
                ),
                (
                    f"Hello {name}, your consistency is inspiring! 🌠 Your timely support helps us plan better for our community initiatives. "
                    f"We're looking forward to your contribution of ₹{amount} in {days_until_due} days. Thanks for leading by example!"
                ),
                (
                    f"Greetings {name}! Just a quick note to say we appreciate you. Your reliable contributions make a real difference. "
                    f"Your next payment of ₹{amount} is coming up in {days_until_due} days. Thank you for being someone we can count on!"
                )
            ]
            return random.choice(templates)
        
        # 2. SOCIAL PROOF (For Neutral/Occasional Delay)
        elif classification == "Occasional Delay":
            templates = [
                (
                    f"Hello {name}, did you know that 92% of our community members have contributed this month? "
                    f"Your support of ₹{amount} (due in {days_until_due} days) makes a huge difference in achieving our collective goals. "
                    f"Join your neighbors in making an impact today!"
                ),
                (
                    f"Hi {name}, our community is coming together to reach our monthly goal! We're almost there. "
                    f"Your contribution of ₹{amount} (due in {days_until_due} days) would overlap perfectly with others giving this week. "
                    f"Let's make a difference together."
                ),
                (
                    f"Dear {name}, most members find it easiest to contribute early in the week. "
                    f"Your upcoming payment of ₹{amount} is due in {days_until_due} days. "
                    f"Join the majority of our community in staying current and supporting our shared vision!"
                )
            ]
            return random.choice(templates)
        
        # 3. EMPATHY & SUPPORT (For High-Risk/Struggling Members)
        # Avoid shame, focus on support and agency
        else:
            if days_until_due <= 3:
                templates = [
                    (
                        f"Dear {name}, we understand that times can be tough. We value you as a member of our family, regardless of financial status. "
                        f"If you're able to contribute your ₹{amount} coming due in {days_until_due} days, it would be greatly appreciated. "
                        f"If you need more time or assistance, please just reply to this message—we are here to support you, not judge you."
                    ),
                    (
                        f"Hi {name}, sending you warm wishes. We know managing expenses can be stressful sometimes. "
                        f"Your contribution of ₹{amount} is coming due, but your well-being comes first. "
                        f"If you can make the payment, great! If not, let's chat about how we can support you."
                    )
                ]
                return random.choice(templates)
            else:
                templates = [
                    (
                        f"Hi {name}, we're checking in to see how you're doing. "
                        f"Your managed contribution is coming up in {days_until_due} days. "
                        f"Please know that your presence in our community matters more than money. "
                        f"Let us know if we can help facilitate your payment in a way that works for you."
                    ),
                    (
                        f"Hello {name}, just a gentle nudge about your upcoming contribution of ₹{amount}. "
                        f"We want to make sure you feel supported in our community. "
                        f"If there's anything we can do to make this easier for you, please reach out."
                    )
                ]
                return random.choice(templates)
    
    @staticmethod
    def analyze_payment_patterns(contributions: List[dict]) -> Dict:
        """
        Analyze payment timing patterns to find preferences
        """
        if not contributions:
            return {"pattern": "No data", "preferred_day": None}
        
        payment_days = []
        payment_delays = []
        
        for c in contributions:
            if c.get("paid_date"):
                paid_date = datetime.strptime(c["paid_date"], "%Y-%m-%d")
                due_date = datetime.strptime(c["due_date"], "%Y-%m-%d")
                
                # Day of month when paid
                payment_days.append(paid_date.day)
                
                # Delay in days
                delay = (paid_date - due_date).days
                payment_delays.append(delay)
        
        if not payment_days:
            return {"pattern": "No payments yet", "preferred_day": None}
        
        # Find most common payment day
        preferred_day = statistics.mode(payment_days) if payment_days else None
        avg_delay = statistics.mean(payment_delays) if payment_delays else 0
        
        # Determine pattern
        if avg_delay <= 2:
            pattern = "On-time payer"
        elif avg_delay <= 7:
            pattern = "Early week delay"
        elif avg_delay <= 15:
            pattern = "Mid-month delay"
        else:
            pattern = "Extended delay"
        
        return {
            "pattern": pattern,
            "preferred_day": preferred_day,
            "average_delay": round(avg_delay, 1),
            "consistency": "High" if len(set(payment_days)) <= 3 else "Variable"
        }
    
    @staticmethod
    def calculate_member_insights(member: dict, contributions: List[dict]) -> Dict:
        """
        Generate comprehensive insights for a member
        """
        risk_score = IntelligenceEngine.calculate_risk_score(contributions, member)
        prediction = IntelligenceEngine.predict_delay_likelihood(contributions, member)
        patterns = IntelligenceEngine.analyze_payment_patterns(contributions)
        
        # Calculate contribution health
        if risk_score < 30:
            health = "Excellent"
        elif risk_score < 60:
            health = "Good"
        elif risk_score < 80:
            health = "Needs Attention"
        else:
            health = "Critical"
        
        # Generate recommendation
        if risk_score < 30:
            recommendation = "No action needed. Continue standard reminders."
        elif risk_score < 60:
            recommendation = "Send reminder 3-5 days before due date."
        elif risk_score < 80:
            recommendation = "Send early reminder (7 days before) and follow-up."
        else:
            recommendation = "Proactive outreach recommended. Consider personal contact."
        
        return {
            "risk_score": round(risk_score, 1),
            "health_status": health,
            "prediction": prediction,
            "payment_patterns": patterns,
            "recommendation": recommendation,
            "total_contributions": len(contributions),
            "paid_count": sum(1 for c in contributions if c.get("paid_date")),
            "success_rate": round((sum(1 for c in contributions if c.get("paid_date")) / len(contributions) * 100), 1) if contributions else 0
        }
