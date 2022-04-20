import { Row, Col } from 'antd';
import ApexActivityChart from "./components/charts.js";
import SummaryCard from "./components/summaryCard.js";
import ServerStats from "./components/serverCard.js";
import MapChart from "./components/map.js";
import Clock from "./components/clock.js";
import "./dashboard.css"
import React from 'react';

class Dashboard extends React.Component{
    constructor(){
        super();
        this.state = {}
    }
    render(){
        return <div>
        <Row type="flex" gutter={16}>
            <Col xs span={8} ><Clock /></Col>
            <Col xs span={8}>
                <ServerStats />
            </Col>
            <Col xs span={8}>
                <SummaryCard />
            </Col>
        </Row>
        <Row type="flex" gutter={16} >
            <Col span={12} style={{border: "1px solid"}}>
                <ApexActivityChart 
                prediction={this.state.prediction}
                fraud={this.state.fraud}
                categories={this.state.categories}/>
            </Col>
            <Col span={12} style={{border: "1px solid"}}><MapChart /></Col>
        </Row>
  </div>
    }
}
export default Dashboard;
