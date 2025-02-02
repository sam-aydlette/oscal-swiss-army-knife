# System Status Report

<div style="display: flex; align-items: center; background-color: #d9f1fd; padding: 20px; margin-bottom: 30px;">
    <h1 style="margin: 0; color: #162e51;">System Name and ID</h1>
</div>

## Overview
<div style="background-color: white; padding: 20px; border-radius: 4px;">
System overview and key information goes here. This section provides context about the system's purpose and current status.
</div>

### Finding Analysis

<div style="background-color: white; padding: 20px; border-radius: 4px;">
    <h4>Six Month Finding Trends</h4>
    ```mermaid
    %%{init: {
      'theme': 'base',
      'themeVariables': {
        'primaryColor': '#1a4480',
        'primaryTextColor': '#454545',
        'primaryBorderColor': '#162e51',
        'lineColor': '#0a90b7',
        'secondaryColor': '#d9f1fd',
        'tertiaryColor': '#c71f25'
      }
    }}%%

    xychart-beta
        title "Six Month Finding Trends"
        x-axis [Aug, Sep, Oct, Nov, Dec, Jan]
        y-axis "Number of Findings" 0 --> 100
        bar [10, 15, 12, 8, 11, 14] "Critical"
        bar [20, 25, 18, 22, 19, 21] "High"
        bar [30, 28, 32, 25, 29, 27] "Medium"
        bar [15, 12, 14, 18, 13, 16] "Low"
        line [75, 80, 76, 73, 72, 78] "Total Findings"
        line [70, 70, 70, 70, 70, 70] "Baseline"
        line [84, 84, 84, 84, 84, 84] "Threshold (+20%)"
    ```
    
    **Key Observations:**
    - Total findings remain below threshold but above baseline
    - Critical findings showed slight increase in January
    - Medium findings consistently represent largest category
</div>

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-top: 20px;">
    <div style="background-color: white; padding: 20px; border-radius: 4px;">
        <h2 style="color: #1a4480;">Items to Investigate</h2>
        <p>Key items that require further investigation:</p>
        <ul style="color: #454545;">
            <li>**High Priority:** Network latency spikes detected in East region</li>
            <li>**Medium Priority:** Database optimization needed for reporting queries</li>
            <li>**Low Priority:** Update SSL certificates (due in 90 days)</li>
        </ul>
    </div>
    <div style="background-color: white; padding: 20px; border-radius: 4px;">
        <h2 style="color: #1a4480;">Customers</h2>
        <p>Current customer metrics and status:</p>
        <ul style="color: #454545;">
            <li>**Active Users:** 1,234 (+5% from last month)</li>
            <li>**Service Uptime:** 99.99% (meeting SLA)</li>
            <li>**Support Tickets:** 5 open, 45 closed this month</li>
        </ul>
    </div>
</div>

---

<div style="background-color: #f2f2f2; padding: 20px; margin-top: 40px; border-radius: 4px;">
<small>

**Report Information**
- Generated: January 31, 2025
- Document Version: 1.0
- Classification: For Official Use Only
- System ID: [System-ID-Here]

</small>
</div>