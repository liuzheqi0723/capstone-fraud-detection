import { Card } from 'antd';
import ApexCharts from "react-apexcharts";
import React from 'react';
class getSummaryCard extends React.Component{

    constructor(props){
        super(props);
        this.state = {
            fraud: 0,
            auth: 0
        }
    }

    componentDidMount(){
        fetch("http://localhost:5000/summary")
            .then(res=>res.json()).then(
                result => {
                    this.setState(
                        {
                        fraud: result.fraud_cnt,
                        auth: result.auth_cnt
                        }
                    )
                }
            )
    }
    render(){
        return (
            <Card title="Total cases processed" style={{height : "100%"}}> <ApexCharts
            type = "donut"
            options= {{
                labels : ['authenticate', 'fraud'],
            }}
            series={[this.state.auth, this.state.fraud]}
            width={"100%"}/></Card>
        )}
    }
    

export default getSummaryCard;