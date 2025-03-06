export default {
    menu: {
        'Large Language Models': '大语言模型',
        'Computer Vision Models': '计算机视觉模型',
        'Automated Diagnosis': '自动诊断',
        'LLaMMA-CT': 'LLM大型语言模型',
        'Real-Time Q&A': '实时问答',
        'IsoCenter Positioning': '等中心定位',
        'CT Range Determination': '范围确定',
        'Lung Nodule Detection': '肺结节检测'
    },
    welcome: {
        title: '欢迎使用 Agentographer',
        subtitle: '请从左侧菜单选择功能'
    },
    common: {
        systemTitle: 'AI 医疗助手',
        systemReady: '系统已就绪'
    },
    chat: {
        placeholder: '请输入您的问题，AI会根据您的提问给出回答',
        waitForResponse: '请等待 AI 回答完成后再提问...',
        thinking: 'AI 正在思考中...',
        send: '发送',
        clearChat: '清除对话',
        connecting: '连接中...',
        connected: '已连接',
        disconnected: '未连接',
        startCall: '点击开始与 AI 通话',
        endCall: '通话已结束',
        muted: '已静音',
        unmuted: '已取消静音',
        commonPrompts: '常用提示词',
        pleaseEnterContent: '请输入内容',
        failedToGetResponse: '获取回答失败',
        AnswerStatus:'AI回答请求失败，请重新尝试发送',
        requestFailed: '请求失败',
        chatCleared: '对话已清除',
        onlyImageAllowed: '只能上传图片文件！',
        imageSizeLimitExceeded: '图片必须小于 2MB！',
        imageUploadSuccess: '图片上传成功',
        welcomeMessage: '你好！我是 AI 助手，有什么可以帮助你的吗？',
        prompts: {
            0: '请帮我分析这张CT图像的异常区域',
            1: '这个病例的诊断建议是什么？',
            2: '请解释一下这个医学术语的含义',
            3: '如何预防这种疾病？',
            4: '这种症状需要做哪些检查？',
            5: '这个治疗方案的优缺点是什么？'
        }
    },
    realtimeQA: {
        title: 'AI 语音助手',
        startTip: '点击下方按钮开始通话',
        systemReady: '系统已就绪，点击通话按钮开始对话',
        connected: '已连接',
        disconnected: '未连接',
        connectionFailed: '连接失败',
        wsConnected: 'WebSocket连接成功',
        wsDisconnected: '连接已断开，请重新开始通话',
        wsError: 'WebSocket连接失败',
        initError: '连接服务器失败',
        micPermissionError: '无法访问麦克风，请检查权限设置',
        startCallError: '开始通话失败',
        callStarted: '通话已开始',
        recognitionStarted: '开始语音识别',
        recognitionStopped: '停止语音识别',
        muted: '已静音',
        unmuted: '已取消静音',
        aiResponding: 'AI正在回答您的问题请稍后！',
        welcomeTitle: 'AI 语音助手',
        welcomeSubtitle: '点击下方按钮开始与 AI 进行语音对话，支持实时语音识别和合成',
        voiceChanged: '已切换语音',
        rateChanged: '已设置语速为 {rate}x',
        speechRecognitionError: '语音识别出错，请重试'
    }
} 