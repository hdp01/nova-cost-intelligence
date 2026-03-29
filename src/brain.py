import boto3
import json

class CostBrain:
    def __init__(self):
        self.bedrock = boto3.client('bedrock-runtime')
        self.model_id = "amazon.nova-micro-v1:0"

    def get_ai_advice(self, raw_data):
        has_waste = (raw_data['ebs_waste_count'] > 0 or 
                     len(raw_data['s3_buckets_no_lifecycle']) > 0)
        
        status_context = "WASTE_DETECTED" if has_waste else "OPTIMIZED"

        prompt = f"""
        You are a Senior FinOps Engineer. Analyze this AWS operational data:
        {json.dumps(raw_data, default=str)}

        ACCOUNT STATUS: {status_context}

        INSTRUCTIONS:
        1. If status is WASTE_DETECTED: Identify the top leaks and give 3 immediate 'Quick Win' steps.
        2. If status is OPTIMIZED: Congratulate the user on high infrastructure hygiene. Suggest one 'Advanced' strategy (e.g., AWS Graviton, Spot Instances, or Savings Plans) for further marginal gains.
        3. Always provide a 'Risk Score' (1-10) where 1 is perfect and 10 is critical.
        4. Keep the output professional, concise, and formatted for a terminal dashboard.
        """
        
        try:
            response = self.bedrock.converse(
                modelId=self.model_id,
                messages=[{"role": "user", "content": [{"text": prompt}]}]
            )
            return response['output']['message']['content'][0]['text']
        except Exception as e:
            return f"AI Analysis Error: {str(e)}"