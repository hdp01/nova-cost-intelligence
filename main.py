import os
from dotenv import load_dotenv
from src.collector import AWSCollector
from src.brain import CostBrain
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

load_dotenv()

def run_app():
    console = Console()
    collector = AWSCollector()
    brain = CostBrain()

    console.print("\n[bold purple]Commencing AI-Powered Cloud Financial Audit...[/bold purple]\n")

    with console.status("[bold green]Accessing AWS Billing APIs...") as status:
        spend_data = collector.get_monthly_spend()
        ebs_waste = collector.get_unattached_volumes()
        rds_data = collector.get_rds_info()
        s3_waste = collector.get_s3_waste()

    service_totals = {}
    for period in spend_data.get('ResultsByTime', []):
        for group in period.get('Groups', []):
            service_name = group['Keys'][0]
            amount = float(group['Metrics']['UnblendedCost']['Amount'])
            service_totals[service_name] = service_totals.get(service_name, 0) + amount

    grand_total = sum(service_totals.values())

    table = Table(title="Total Spend (Last 30 Days)", header_style="bold magenta")
    table.add_column("Service", style="cyan")
    table.add_column("Cost (USD)", justify="right", style="green")

    sorted_services = sorted(service_totals.items(), key=lambda x: x[1], reverse=True)

    for service, total in sorted_services:
        if total >= 0.00:
            table.add_row(service, f"${total:.4f}")

    table.add_section()
    table.add_row("[bold yellow]GRAND TOTAL[/bold yellow]", f"[bold yellow]${grand_total:.2f}[/bold yellow]")

    console.print(table)

    clean_spend_totals = {k: round(v, 4) for k, v in service_totals.items()}

    raw_context = {
        "grand_total": round(grand_total, 2),
        "monthly_spend_totals": clean_spend_totals,
        "ebs_waste_count": len(ebs_waste['Volumes']),
        "rds_instances": [{"ID": d['DBInstanceIdentifier'], "Status": d['DBInstanceStatus']} for d in rds_data],
        "s3_buckets_no_lifecycle": s3_waste
    }

    console.print("\n[bold yellow]Consulting Amazon Nova AI...[/bold yellow]")

    with console.status("[italic]Analyzing cost patterns...") as status:
        ai_insight = brain.get_ai_advice(raw_context)

    console.print(Panel(
        ai_insight,
        title="[bold green]Nova AI: FinOps Strategic Report[/bold green]",
        border_style="bold blue",
        padding=(1, 2)
    ))

if __name__ == "__main__":
    run_app()