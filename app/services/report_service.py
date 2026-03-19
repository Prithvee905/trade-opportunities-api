from typing import List, Dict

def build_markdown_report(sector: str, news_data: List[Dict[str, str]], ai_analysis: str) -> str:
    """
    Constructs the final markdown report structured gracefully.
    """
    
    # Capitalize sector name nicely
    formatted_sector = sector.title()
    
    report = f"# Trade Opportunities Report\n\n"
    report += f"## Sector\n{formatted_sector}\n\n"
    
    report += "## Market News\n"
    if not news_data:
        report += "No recent news found.\n"
    else:
        for item in news_data:
            report += f"- **[{item['title']}]({item['url']})**: {item['summary']}\n"
            
    report += f"\n## AI Market Analysis\n"
    report += f"{ai_analysis}\n"
    
    return report
