import { Layout, Menu } from 'antd';
import {
  MenuUnfoldOutlined,
  MenuFoldOutlined,
  UserOutlined,
  VideoCameraOutlined,
} from '@ant-design/icons';
import React from 'react';
import "./layout.css";
import {
    Link,
    Routes,
    Route,
  } from "react-router-dom"

import Models from "../Models/models"
import Dashboard from "../Dashboard/dashboard"

const { Header, Sider, Content } = Layout;

class SiderLayout extends React.Component {
  state = {
    collapsed: false,
  };

  toggle = () => {
    this.setState({
      collapsed: !this.state.collapsed,
    });
  };

  render() {
    return (
      <Layout style={{minHeight : 800}}>
        <Sider trigger={null} collapsible collapsed={this.state.collapsed}>
          <div className="logo" />
          <Menu theme="dark" mode="inline" defaultSelectedKeys={['1']}>
            <Menu.Item key="1" icon={<UserOutlined />}>
              <Link to="/dashboard"> Dashboard </Link>
            </Menu.Item>
            <Menu.Item key="2" icon={<VideoCameraOutlined />}>
            <Link to="/models"> Models </Link>
            </Menu.Item>
          </Menu>
        </Sider>
        <Layout className="site-layout">
          <Header className="site-layout-background" style={{ padding: 0 }}>
            {React.createElement(this.state.collapsed ? MenuUnfoldOutlined : MenuFoldOutlined, {
              className: 'trigger',
              onClick: this.toggle,
            })}
          </Header>
          <Content
            className="site-layout-background"
            style={{
              margin: '24px 16px',
              padding: 24,
            }}
          >
            <Routes>
                <Route path="/dashboard" style={{ height: "100%" }} element={<Dashboard />} />
                <Route path="/" style={{ height: "100%" }} element={<Dashboard />} />
                <Route path="/models" style={{ height: "100%" }} element={<Models />} />
            </Routes>
          </Content>
        </Layout>
      </Layout>
    );
  }
}

export default SiderLayout;