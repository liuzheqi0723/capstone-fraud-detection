import { Card } from 'antd';
import ApexCharts from "react-apexcharts";

export default function getSummaryCard(){
    return (
        <Card title="Total cases processed" style={{height : "100%"}}> <ApexCharts
        type = "donut"
        options= {{
            labels : ['a', 'b']
        }}
        series={[200, 2400]}
        height={"100%"}
        width={"100%"}/></Card>
    )}