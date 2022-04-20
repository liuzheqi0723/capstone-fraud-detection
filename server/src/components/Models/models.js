import { Upload, message, Button } from 'antd';
import { UploadOutlined } from '@ant-design/icons';

const props = {
    name: 'file',
    action: 'http://127.0.0.1:5000/models',
    headers: {
      authorization: 'authorization-text',
      'Access-Control-Allow-Origin' : '*'
    },
    method: 'POST',
    onChange(info) {
      if (info.file.status !== 'uploading') {
        console.log(info.file, info.fileList);
      }
      if (info.file.status === 'done') {
        message.success(`${info.file.name} file uploaded successfully`);
      } else if (info.file.status === 'error') {
        message.error(`${info.file.name} file upload failed.`);
      }
    },
  };

export default function getModelsComponent(){
    return <h1> 
    <Upload {...props}>
        <Button icon={<UploadOutlined />}>Click to Upload</Button>
    </Upload>
    </h1>
}