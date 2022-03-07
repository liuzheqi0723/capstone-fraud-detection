import { Row, Col } from 'antd';
import ApexActivityChart from "./components/charts.js";
import SummaryCard from "./components/summaryCard.js";
import ServerStats from "./components/serverCard.js";
import MapChart from "./components/map.js";
export default function getDashBoardElement(){
    return <div>
        <Row style={{ height: "10vn", alignItems: "center" }}>
            <Col type="flex" style={{ height: "100%" }} span={8}>1</Col>
            <Col type="flex" style={{ height: "100%" }} span={8}>
                <ServerStats />
            </Col>
            <Col type="flex" style={{ height: "100%" }} span={8}>
                <SummaryCard />
            </Col>
        </Row>
        <Row style={{ height: "60vh", alignItems: "center" }}>
            <Col span={12}><ApexActivityChart /></Col>
            <Col span={12}><MapChart /></Col>
        </Row>
  </div>
}