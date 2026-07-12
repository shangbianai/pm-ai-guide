// 页面数据
const pageData = {
    home: {
        title: '首页',
        subtitle: '欢迎使用移动端管理系统',
        content: `
            <div class="mobile-page">
                <div class="mobile-header">
                    <h1>首页</h1>
                    <div class="subtitle">欢迎使用移动端管理系统</div>
                </div>
                <div class="mobile-content">
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-number">1,234</div>
                            <div class="stat-label">总用户数</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">567</div>
                            <div class="stat-label">今日订单</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">89.2%</div>
                            <div class="stat-label">转化率</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">¥12,345</div>
                            <div class="stat-label">今日收入</div>
                        </div>
                    </div>
                    
                    <div class="card">
                        <div class="card-header">
                            <div>
                                <div class="card-title">快速操作</div>
                                <div class="card-subtitle">常用功能快捷入口</div>
                            </div>
                        </div>
                        <div class="list-item" onclick="loadPage('product-add')">
                            <div class="list-item-icon">
                                <i class="fas fa-plus"></i>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">添加商品</div>
                                <div class="list-item-subtitle">快速上架新产品</div>
                            </div>
                            <div class="list-item-arrow">
                                <i class="fas fa-chevron-right"></i>
                            </div>
                        </div>
                        <div class="list-item" onclick="loadPage('order-list')">
                            <div class="list-item-icon">
                                <i class="fas fa-list-alt"></i>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">查看订单</div>
                                <div class="list-item-subtitle">管理所有订单状态</div>
                            </div>
                            <div class="list-item-arrow">
                                <i class="fas fa-chevron-right"></i>
                            </div>
                        </div>
                        <div class="list-item" onclick="loadPage('sales-chart')">
                            <div class="list-item-icon">
                                <i class="fas fa-chart-line"></i>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">销售统计</div>
                                <div class="list-item-subtitle">查看销售数据分析</div>
                            </div>
                            <div class="list-item-arrow">
                                <i class="fas fa-chevron-right"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `
    },
    
    profile: {
        title: '个人资料',
        subtitle: '管理您的个人信息',
        content: `
            <div class="mobile-page">
                <div class="mobile-header">
                    <h1>个人资料</h1>
                    <div class="subtitle">管理您的个人信息</div>
                </div>
                <div class="mobile-content">
                    <div class="card">
                        <div class="card-header">
                            <div class="card-title">基本信息</div>
                        </div>
                        <div class="form-group">
                            <label class="form-label">头像</label>
                            <div style="text-align: center; padding: 20px;">
                                <div class="profile-avatar">
                                    <i class="fas fa-user"></i>
                                </div>
                                <div style="margin-top: 10px;">
                                    <button class="btn btn-secondary">更换头像</button>
                                </div>
                            </div>
                        </div>
                        <div class="form-group">
                            <label class="form-label">姓名</label>
                            <input type="text" class="form-input" value="张三" placeholder="请输入姓名">
                        </div>
                        <div class="form-group">
                            <label class="form-label">手机号</label>
                            <input type="tel" class="form-input" value="138****8888" placeholder="请输入手机号">
                        </div>
                        <div class="form-group">
                            <label class="form-label">邮箱</label>
                            <input type="email" class="form-input" value="zhangsan@example.com" placeholder="请输入邮箱">
                        </div>
                        <div class="form-group">
                            <label class="form-label">职位</label>
                            <input type="text" class="form-input" value="产品经理" placeholder="请输入职位">
                        </div>
                        <button class="btn" style="width: 100%;">保存修改</button>
                    </div>
                </div>
            </div>
        `
    },
    
    settings: {
        title: '设置',
        subtitle: '系统设置与偏好',
        content: `
            <div class="mobile-page">
                <div class="mobile-header">
                    <h1>设置</h1>
                    <div class="subtitle">系统设置与偏好</div>
                </div>
                <div class="mobile-content">
                    <div class="card">
                        <div class="list-item">
                            <div class="list-item-icon">
                                <i class="fas fa-bell"></i>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">消息通知</div>
                                <div class="list-item-subtitle">管理推送通知设置</div>
                            </div>
                            <div class="list-item-arrow">
                                <i class="fas fa-chevron-right"></i>
                            </div>
                        </div>
                        <div class="list-item">
                            <div class="list-item-icon">
                                <i class="fas fa-shield-alt"></i>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">隐私安全</div>
                                <div class="list-item-subtitle">账户安全设置</div>
                            </div>
                            <div class="list-item-arrow">
                                <i class="fas fa-chevron-right"></i>
                            </div>
                        </div>
                        <div class="list-item">
                            <div class="list-item-icon">
                                <i class="fas fa-language"></i>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">语言设置</div>
                                <div class="list-item-subtitle">简体中文</div>
                            </div>
                            <div class="list-item-arrow">
                                <i class="fas fa-chevron-right"></i>
                            </div>
                        </div>
                        <div class="list-item">
                            <div class="list-item-icon">
                                <i class="fas fa-moon"></i>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">深色模式</div>
                                <div class="list-item-subtitle">切换深色主题</div>
                            </div>
                            <div class="list-item-arrow">
                                <i class="fas fa-chevron-right"></i>
                            </div>
                        </div>
                    </div>
                    
                    <div class="card">
                        <div class="list-item">
                            <div class="list-item-icon">
                                <i class="fas fa-question-circle"></i>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">帮助中心</div>
                                <div class="list-item-subtitle">使用指南与常见问题</div>
                            </div>
                            <div class="list-item-arrow">
                                <i class="fas fa-chevron-right"></i>
                            </div>
                        </div>
                        <div class="list-item">
                            <div class="list-item-icon">
                                <i class="fas fa-info-circle"></i>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">关于我们</div>
                                <div class="list-item-subtitle">版本 1.0.0</div>
                            </div>
                            <div class="list-item-arrow">
                                <i class="fas fa-chevron-right"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `
    },
    
    products: {
        title: '商品管理',
        subtitle: '商品管理首页',
        content: `
            <div class="mobile-page">
                <div class="mobile-header">
                    <h1>商品管理</h1>
                    <div class="subtitle">商品管理首页</div>
                </div>
                <div class="mobile-content">
                    <div class="card">
                        <div class="card-header">
                            <div class="card-title">快速操作</div>
                        </div>
                        <div class="list-item" onclick="loadPage('product-list')">
                            <div class="list-item-icon">
                                <i class="fas fa-list"></i>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">商品列表</div>
                                <div class="list-item-subtitle">查看和管理所有商品</div>
                            </div>
                            <div class="list-item-arrow">
                                <i class="fas fa-chevron-right"></i>
                            </div>
                        </div>
                        <div class="list-item" onclick="loadPage('product-add')">
                            <div class="list-item-icon">
                                <i class="fas fa-plus"></i>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">添加商品</div>
                                <div class="list-item-subtitle">创建新的商品</div>
                            </div>
                            <div class="list-item-arrow">
                                <i class="fas fa-chevron-right"></i>
                            </div>
                        </div>
                    </div>
                    
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-number">8</div>
                            <div class="stat-label">商品总数</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">156</div>
                            <div class="stat-label">总库存</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">¥12,345</div>
                            <div class="stat-label">商品总价值</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">5</div>
                            <div class="stat-label">商品分类</div>
                        </div>
                    </div>
                </div>
            </div>
        `
    },
    
    'product-list': {
        title: '商品列表',
        subtitle: '管理所有商品',
        content: `
            <div class="mobile-page">
                <div class="mobile-header">
                    <h1>商品列表</h1>
                    <div class="subtitle">管理所有商品</div>
                </div>
                <div class="mobile-content">
                    <div class="card">
                        <div class="card-header">
                            <div>
                                <div class="card-title">商品管理</div>
                                <div class="card-subtitle">共 8 个商品</div>
                            </div>
                            <button class="btn" onclick="loadPage('product-add')">添加商品</button>
                        </div>
                    </div>
                    
                    <div class="card">
                        <div class="list-item" onclick="showProductDetail('时尚T恤')">
                            <div class="list-item-icon">
                                <i class="fas fa-tshirt"></i>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">时尚T恤</div>
                                <div class="list-item-subtitle">库存: 156件 | 价格: ¥89 | 分类: 服装</div>
                            </div>
                            <div class="list-item-arrow">
                                <i class="fas fa-chevron-right"></i>
                            </div>
                        </div>
                        <div class="list-item" onclick="showProductDetail('运动鞋')">
                            <div class="list-item-icon">
                                <i class="fas fa-shoe-prints"></i>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">运动鞋</div>
                                <div class="list-item-subtitle">库存: 89双 | 价格: ¥299 | 分类: 鞋类</div>
                            </div>
                            <div class="list-item-arrow">
                                <i class="fas fa-chevron-right"></i>
                            </div>
                        </div>
                        <div class="list-item" onclick="showProductDetail('智能手机')">
                            <div class="list-item-icon">
                                <i class="fas fa-mobile-alt"></i>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">智能手机</div>
                                <div class="list-item-subtitle">库存: 23台 | 价格: ¥2999 | 分类: 数码</div>
                            </div>
                            <div class="list-item-arrow">
                                <i class="fas fa-chevron-right"></i>
                            </div>
                        </div>
                        <div class="list-item" onclick="showProductDetail('笔记本电脑')">
                            <div class="list-item-icon">
                                <i class="fas fa-laptop"></i>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">笔记本电脑</div>
                                <div class="list-item-subtitle">库存: 12台 | 价格: ¥5999 | 分类: 数码</div>
                            </div>
                            <div class="list-item-arrow">
                                <i class="fas fa-chevron-right"></i>
                            </div>
                        </div>
                        <div class="list-item" onclick="showProductDetail('蓝牙耳机')">
                            <div class="list-item-icon">
                                <i class="fas fa-headphones"></i>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">蓝牙耳机</div>
                                <div class="list-item-subtitle">库存: 67个 | 价格: ¥199 | 分类: 数码</div>
                            </div>
                            <div class="list-item-arrow">
                                <i class="fas fa-chevron-right"></i>
                            </div>
                        </div>
                        <div class="list-item" onclick="showProductDetail('护肤套装')">
                            <div class="list-item-icon">
                                <i class="fas fa-spa"></i>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">护肤套装</div>
                                <div class="list-item-subtitle">库存: 45套 | 价格: ¥399 | 分类: 美妆</div>
                            </div>
                            <div class="list-item-arrow">
                                <i class="fas fa-chevron-right"></i>
                            </div>
                        </div>
                        <div class="list-item" onclick="showProductDetail('咖啡机')">
                            <div class="list-item-icon">
                                <i class="fas fa-coffee"></i>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">咖啡机</div>
                                <div class="list-item-subtitle">库存: 18台 | 价格: ¥1299 | 分类: 家居</div>
                            </div>
                            <div class="list-item-arrow">
                                <i class="fas fa-chevron-right"></i>
                            </div>
                        </div>
                        <div class="list-item" onclick="showProductDetail('运动手表')">
                            <div class="list-item-icon">
                                <i class="fas fa-clock"></i>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">运动手表</div>
                                <div class="list-item-subtitle">库存: 34个 | 价格: ¥899 | 分类: 数码</div>
                            </div>
                            <div class="list-item-arrow">
                                <i class="fas fa-chevron-right"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `
    },
    
    'product-add': {
        title: '添加商品',
        subtitle: '创建新商品',
        content: `
            <div class="mobile-page">
                <div class="mobile-header">
                    <h1>添加商品</h1>
                    <div class="subtitle">创建新商品</div>
                </div>
                <div class="mobile-content">
                    <div class="card">
                        <div class="form-group">
                            <label class="form-label">商品图片</label>
                            <div style="text-align: center; padding: 20px; border: 2px dashed #ddd; border-radius: 8px; cursor: pointer;" onclick="uploadImage()">
                                <i class="fas fa-camera" style="font-size: 32px; color: #ccc; margin-bottom: 10px;"></i>
                                <div style="color: #666;">点击上传商品图片</div>
                                <div style="font-size: 12px; color: #999; margin-top: 5px;">支持 JPG、PNG 格式，最大 5MB</div>
                            </div>
                        </div>
                        <div class="form-group">
                            <label class="form-label">商品名称 <span style="color: red;">*</span></label>
                            <input type="text" class="form-input" placeholder="请输入商品名称" id="productName">
                        </div>
                        <div class="form-group">
                            <label class="form-label">商品分类 <span style="color: red;">*</span></label>
                            <select class="form-input" id="productCategory">
                                <option value="">请选择分类</option>
                                <option value="服装">服装</option>
                                <option value="数码">数码</option>
                                <option value="家居">家居</option>
                                <option value="美妆">美妆</option>
                                <option value="鞋类">鞋类</option>
                                <option value="配饰">配饰</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label class="form-label">商品价格 <span style="color: red;">*</span></label>
                            <div style="display: flex; align-items: center;">
                                <span style="margin-right: 10px; color: #666;">¥</span>
                                <input type="number" class="form-input" placeholder="0.00" id="productPrice" style="flex: 1;">
                            </div>
                        </div>
                        <div class="form-group">
                            <label class="form-label">库存数量 <span style="color: red;">*</span></label>
                            <input type="number" class="form-input" placeholder="请输入库存数量" id="productStock">
                        </div>
                        <div class="form-group">
                            <label class="form-label">商品规格</label>
                            <input type="text" class="form-input" placeholder="如：颜色、尺寸等" id="productSpec">
                        </div>
                        <div class="form-group">
                            <label class="form-label">商品描述</label>
                            <textarea class="form-input" rows="4" placeholder="请输入商品详细描述" id="productDesc"></textarea>
                        </div>
                        <div class="form-group">
                            <label class="form-label">商品状态</label>
                            <div style="display: flex; gap: 15px;">
                                <label style="display: flex; align-items: center; cursor: pointer;">
                                    <input type="radio" name="status" value="active" checked style="margin-right: 8px;">
                                    <span>上架</span>
                                </label>
                                <label style="display: flex; align-items: center; cursor: pointer;">
                                    <input type="radio" name="status" value="inactive" style="margin-right: 8px;">
                                    <span>下架</span>
                                </label>
                            </div>
                        </div>
                        <div style="display: flex; gap: 10px; margin-top: 20px;">
                            <button class="btn btn-secondary" style="flex: 1;" onclick="resetForm()">重置</button>
                            <button class="btn" style="flex: 1;" onclick="submitProduct()">创建商品</button>
                        </div>
                    </div>
                </div>
            </div>
        `
    },
    
    orders: {
        title: '订单管理',
        subtitle: '订单管理首页',
        content: `
            <div class="mobile-page">
                <div class="mobile-header">
                    <h1>订单管理</h1>
                    <div class="subtitle">订单管理首页</div>
                </div>
                <div class="mobile-content">
                    <div class="card">
                        <div class="card-header">
                            <div class="card-title">快速操作</div>
                        </div>
                        <div class="list-item" onclick="loadPage('order-list')">
                            <div class="list-item-icon">
                                <i class="fas fa-list-alt"></i>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">订单列表</div>
                                <div class="list-item-subtitle">查看和管理所有订单</div>
                            </div>
                            <div class="list-item-arrow">
                                <i class="fas fa-chevron-right"></i>
                            </div>
                        </div>
                        <div class="list-item" onclick="loadPage('order-detail')">
                            <div class="list-item-icon">
                                <i class="fas fa-file-alt"></i>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">订单详情</div>
                                <div class="list-item-subtitle">查看订单详细信息</div>
                            </div>
                            <div class="list-item-arrow">
                                <i class="fas fa-chevron-right"></i>
                            </div>
                        </div>
                    </div>
                    
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-number">12</div>
                            <div class="stat-label">总订单数</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">3</div>
                            <div class="stat-label">待发货</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">2</div>
                            <div class="stat-label">待付款</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">7</div>
                            <div class="stat-label">已完成</div>
                        </div>
                    </div>
                </div>
            </div>
        `
    },
    
    'order-list': {
        title: '订单列表',
        subtitle: '查看所有订单',
        content: `
            <div class="mobile-page">
                <div class="mobile-header">
                    <h1>订单列表</h1>
                    <div class="subtitle">查看所有订单</div>
                </div>
                <div class="mobile-content">
                    <div class="card">
                        <div class="card-header">
                            <div>
                                <div class="card-title">订单筛选</div>
                                <div class="card-subtitle">共 12 个订单</div>
                            </div>
                        </div>
                        <div style="display: flex; gap: 10px; margin-bottom: 15px;">
                            <button class="btn btn-secondary" style="flex: 1; font-size: 14px; padding: 8px 12px;" onclick="filterOrders('all')">全部</button>
                            <button class="btn btn-secondary" style="flex: 1; font-size: 14px; padding: 8px 12px;" onclick="filterOrders('pending')">待付款</button>
                            <button class="btn btn-secondary" style="flex: 1; font-size: 14px; padding: 8px 12px;" onclick="filterOrders('shipping')">待发货</button>
                            <button class="btn btn-secondary" style="flex: 1; font-size: 14px; padding: 8px 12px;" onclick="filterOrders('completed')">已完成</button>
                        </div>
                    </div>
                    
                    <div class="card" id="orderList">
                        <div class="list-item" onclick="loadPage('order-detail')">
                            <div class="list-item-icon" style="background: #ffc107;">
                                <i class="fas fa-clock"></i>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">订单 #20231201001</div>
                                <div class="list-item-subtitle">张三 | ¥299 | 待发货</div>
                                <div style="font-size: 12px; color: #999; margin-top: 2px;">2023-12-01 10:30</div>
                            </div>
                            <div class="list-item-arrow">
                                <i class="fas fa-chevron-right"></i>
                            </div>
                        </div>
                        <div class="list-item" onclick="loadPage('order-detail')">
                            <div class="list-item-icon" style="background: #28a745;">
                                <i class="fas fa-truck"></i>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">订单 #20231201002</div>
                                <div class="list-item-subtitle">李四 | ¥5999 | 已发货</div>
                                <div style="font-size: 12px; color: #999; margin-top: 2px;">2023-12-01 09:15</div>
                            </div>
                            <div class="list-item-arrow">
                                <i class="fas fa-chevron-right"></i>
                            </div>
                        </div>
                        <div class="list-item" onclick="loadPage('order-detail')">
                            <div class="list-item-icon" style="background: #6c757d;">
                                <i class="fas fa-check"></i>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">订单 #20231201003</div>
                                <div class="list-item-subtitle">王五 | ¥89 | 已完成</div>
                                <div style="font-size: 12px; color: #999; margin-top: 2px;">2023-11-30 16:45</div>
                            </div>
                            <div class="list-item-arrow">
                                <i class="fas fa-chevron-right"></i>
                            </div>
                        </div>
                        <div class="list-item" onclick="loadPage('order-detail')">
                            <div class="list-item-icon" style="background: #dc3545;">
                                <i class="fas fa-exclamation"></i>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">订单 #20231201004</div>
                                <div class="list-item-subtitle">赵六 | ¥2999 | 待付款</div>
                                <div style="font-size: 12px; color: #999; margin-top: 2px;">2023-12-01 14:20</div>
                            </div>
                            <div class="list-item-arrow">
                                <i class="fas fa-chevron-right"></i>
                            </div>
                        </div>
                        <div class="list-item" onclick="loadPage('order-detail')">
                            <div class="list-item-icon" style="background: #ffc107;">
                                <i class="fas fa-clock"></i>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">订单 #20231201005</div>
                                <div class="list-item-subtitle">孙七 | ¥199 | 待发货</div>
                                <div style="font-size: 12px; color: #999; margin-top: 2px;">2023-12-01 11:30</div>
                            </div>
                            <div class="list-item-arrow">
                                <i class="fas fa-chevron-right"></i>
                            </div>
                        </div>
                        <div class="list-item" onclick="loadPage('order-detail')">
                            <div class="list-item-icon" style="background: #28a745;">
                                <i class="fas fa-truck"></i>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">订单 #20231201006</div>
                                <div class="list-item-subtitle">周八 | ¥899 | 已发货</div>
                                <div style="font-size: 12px; color: #999; margin-top: 2px;">2023-11-30 20:15</div>
                            </div>
                            <div class="list-item-arrow">
                                <i class="fas fa-chevron-right"></i>
                            </div>
                        </div>
                        <div class="list-item" onclick="loadPage('order-detail')">
                            <div class="list-item-icon" style="background: #6c757d;">
                                <i class="fas fa-check"></i>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">订单 #20231201007</div>
                                <div class="list-item-subtitle">吴九 | ¥399 | 已完成</div>
                                <div style="font-size: 12px; color: #999; margin-top: 2px;">2023-11-30 13:20</div>
                            </div>
                            <div class="list-item-arrow">
                                <i class="fas fa-chevron-right"></i>
                            </div>
                        </div>
                        <div class="list-item" onclick="loadPage('order-detail')">
                            <div class="list-item-icon" style="background: #dc3545;">
                                <i class="fas fa-exclamation"></i>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">订单 #20231201008</div>
                                <div class="list-item-subtitle">郑十 | ¥1299 | 待付款</div>
                                <div style="font-size: 12px; color: #999; margin-top: 2px;">2023-12-01 15:45</div>
                            </div>
                            <div class="list-item-arrow">
                                <i class="fas fa-chevron-right"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `
    },
    
    'order-detail': {
        title: '订单详情',
        subtitle: '订单 #20231201001',
        content: `
            <div class="mobile-page">
                <div class="mobile-header">
                    <h1>订单详情</h1>
                    <div class="subtitle">订单 #20231201001</div>
                </div>
                <div class="mobile-content">
                    <div class="card">
                        <div class="card-header">
                            <div class="card-title">订单状态</div>
                            <div style="background: #ffc107; color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px;">待发货</div>
                        </div>
                        <div style="padding: 15px 0;">
                            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                                <div style="width: 20px; height: 20px; background: #28a745; border-radius: 50%; margin-right: 15px; display: flex; align-items: center; justify-content: center;">
                                    <i class="fas fa-check" style="color: white; font-size: 10px;"></i>
                                </div>
                                <div>
                                    <div style="font-weight: 500;">订单已确认</div>
                                    <div style="font-size: 12px; color: #666;">2023-12-01 10:30</div>
                                </div>
                            </div>
                            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                                <div style="width: 20px; height: 20px; background: #28a745; border-radius: 50%; margin-right: 15px; display: flex; align-items: center; justify-content: center;">
                                    <i class="fas fa-check" style="color: white; font-size: 10px;"></i>
                                </div>
                                <div>
                                    <div style="font-weight: 500;">付款成功</div>
                                    <div style="font-size: 12px; color: #666;">2023-12-01 10:35</div>
                                </div>
                            </div>
                            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                                <div style="width: 20px; height: 20px; background: #ffc107; border-radius: 50%; margin-right: 15px; display: flex; align-items: center; justify-content: center;">
                                    <i class="fas fa-clock" style="color: white; font-size: 10px;"></i>
                                </div>
                                <div>
                                    <div style="font-weight: 500;">待发货</div>
                                    <div style="font-size: 12px; color: #666;">等待处理中</div>
                                </div>
                            </div>
                            <div style="display: flex; align-items: center;">
                                <div style="width: 20px; height: 20px; background: #e9ecef; border-radius: 50%; margin-right: 15px;"></div>
                                <div>
                                    <div style="font-weight: 500; color: #999;">已发货</div>
                                    <div style="font-size: 12px; color: #999;">等待物流更新</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="card">
                        <div class="card-header">
                            <div class="card-title">商品信息</div>
                        </div>
                        <div class="list-item">
                            <div class="list-item-icon">
                                <i class="fas fa-tshirt"></i>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">时尚T恤</div>
                                <div class="list-item-subtitle">颜色: 白色 | 尺寸: L</div>
                                <div style="font-size: 12px; color: #999; margin-top: 2px;">数量: 1件 | 单价: ¥299</div>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-weight: 600; color: var(--accent);">¥299</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="card">
                        <div class="card-header">
                            <div class="card-title">收货信息</div>
                        </div>
                        <div style="padding: 15px 0;">
                            <div style="margin-bottom: 10px;">
                                <strong>收货人:</strong> 张三
                            </div>
                            <div style="margin-bottom: 10px;">
                                <strong>电话:</strong> 138****8888
                            </div>
                            <div>
                                <strong>地址:</strong> 北京市朝阳区某某街道某某小区1号楼101室
                            </div>
                        </div>
                    </div>
                    
                    <div class="card">
                        <div class="card-header">
                            <div class="card-title">物流信息</div>
                        </div>
                        <div style="padding: 15px 0;">
                            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                                <i class="fas fa-truck" style="color: var(--accent); margin-right: 10px;"></i>
                                <div>
                                    <div style="font-weight: 500;">预计发货时间</div>
                                    <div style="font-size: 12px; color: #666;">2023-12-02 09:00</div>
                                </div>
                            </div>
                            <div style="display: flex; align-items: center;">
                                <i class="fas fa-clock" style="color: #ffc107; margin-right: 10px;"></i>
                                <div>
                                    <div style="font-weight: 500;">预计送达时间</div>
                                    <div style="font-size: 12px; color: #666;">2023-12-04 18:00</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="card">
                        <div class="card-header">
                            <div class="card-title">订单金额</div>
                        </div>
                        <div style="padding: 15px 0;">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                                <span>商品金额:</span>
                                <span>¥299.00</span>
                            </div>
                            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                                <span>运费:</span>
                                <span>¥0.00</span>
                            </div>
                            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                                <span>优惠券:</span>
                                <span style="color: #28a745;">-¥10.00</span>
                            </div>
                            <div style="display: flex; justify-content: space-between; font-weight: 600; font-size: 18px; border-top: 1px solid #eee; padding-top: 10px;">
                                <span>实付金额:</span>
                                <span style="color: #dc3545;">¥289.00</span>
                            </div>
                        </div>
                    </div>
                    
                    <div style="display: flex; gap: 10px; margin-top: 20px;">
                        <button class="btn btn-secondary" style="flex: 1;" onclick="contactCustomer()">联系客服</button>
                        <button class="btn" style="flex: 1;" onclick="updateOrderStatus()">更新状态</button>
                    </div>
                </div>
            </div>
        `
    },
    
    analytics: {
        title: '数据分析',
        subtitle: '数据分析首页',
        content: `
            <div class="mobile-page">
                <div class="mobile-header">
                    <h1>数据分析</h1>
                    <div class="subtitle">数据分析首页</div>
                </div>
                <div class="mobile-content">
                    <div class="card">
                        <div class="card-header">
                            <div class="card-title">分析模块</div>
                        </div>
                        <div class="list-item" onclick="loadPage('sales-chart')">
                            <div class="list-item-icon">
                                <i class="fas fa-chart-line"></i>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">销售统计</div>
                                <div class="list-item-subtitle">销售数据分析和趋势</div>
                            </div>
                            <div class="list-item-arrow">
                                <i class="fas fa-chevron-right"></i>
                            </div>
                        </div>
                        <div class="list-item" onclick="loadPage('user-analytics')">
                            <div class="list-item-icon">
                                <i class="fas fa-users"></i>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">用户分析</div>
                                <div class="list-item-subtitle">用户行为数据分析</div>
                            </div>
                            <div class="list-item-arrow">
                                <i class="fas fa-chevron-right"></i>
                            </div>
                        </div>
                    </div>
                    
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-number">¥45,678</div>
                            <div class="stat-label">本月销售额</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">1,234</div>
                            <div class="stat-label">总用户数</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">89.2%</div>
                            <div class="stat-label">转化率</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">12.5%</div>
                            <div class="stat-label">增长率</div>
                        </div>
                    </div>
                </div>
            </div>
        `
    },
    
    'sales-chart': {
        title: '销售统计',
        subtitle: '销售数据分析',
        content: `
            <div class="mobile-page">
                <div class="mobile-header">
                    <h1>销售统计</h1>
                    <div class="subtitle">销售数据分析</div>
                </div>
                <div class="mobile-content">
                    <div class="card">
                        <div class="card-header">
                            <div class="card-title">时间筛选</div>
                        </div>
                        <div style="display: flex; gap: 10px; margin-bottom: 15px;">
                            <button class="btn btn-secondary" style="flex: 1; font-size: 14px; padding: 8px 12px;" onclick="filterSales('today')">今日</button>
                            <button class="btn btn-secondary" style="flex: 1; font-size: 14px; padding: 8px 12px;" onclick="filterSales('week')">本周</button>
                            <button class="btn" style="flex: 1; font-size: 14px; padding: 8px 12px;" onclick="filterSales('month')">本月</button>
                            <button class="btn btn-secondary" style="flex: 1; font-size: 14px; padding: 8px 12px;" onclick="filterSales('year')">本年</button>
                        </div>
                    </div>
                    
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-number">¥45,678</div>
                            <div class="stat-label">本月销售额</div>
                            <div style="font-size: 12px; color: #28a745; margin-top: 5px;">↗ +12.5%</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">234</div>
                            <div class="stat-label">本月订单数</div>
                            <div style="font-size: 12px; color: #28a745; margin-top: 5px;">↗ +8.3%</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">¥195</div>
                            <div class="stat-label">平均客单价</div>
                            <div style="font-size: 12px; color: #28a745; margin-top: 5px;">↗ +3.9%</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">89.2%</div>
                            <div class="stat-label">转化率</div>
                            <div style="font-size: 12px; color: #dc3545; margin-top: 5px;">↘ -2.1%</div>
                        </div>
                    </div>
                    
                    <div class="card">
                        <div class="card-header">
                            <div class="card-title">销售趋势</div>
                        </div>
                        <div class="chart-placeholder">
                            <div style="text-align: center;">
                                <i class="fas fa-chart-line chart-placeholder-icon"></i>
                                <div style="font-weight: 500;">销售趋势图表</div>
                                <div style="font-size: 12px; margin-top: 5px; color: var(--text-muted);">（演示用图表占位）</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="card">
                        <div class="card-header">
                            <div class="card-title">热销商品 TOP5</div>
                        </div>
                        <div class="list-item">
                            <div class="list-item-icon" style="background: #ffd700;">
                                <span style="font-weight: bold; color: white;">1</span>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">时尚T恤</div>
                                <div class="list-item-subtitle">销量: 156件 | 销售额: ¥13,884</div>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 12px; color: #28a745;">+15.2%</div>
                            </div>
                        </div>
                        <div class="list-item">
                            <div class="list-item-icon" style="background: #c0c0c0;">
                                <span style="font-weight: bold; color: white;">2</span>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">运动鞋</div>
                                <div class="list-item-subtitle">销量: 89双 | 销售额: ¥26,611</div>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 12px; color: #28a745;">+8.7%</div>
                            </div>
                        </div>
                        <div class="list-item">
                            <div class="list-item-icon" style="background: #cd7f32;">
                                <span style="font-weight: bold; color: white;">3</span>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">智能手机</div>
                                <div class="list-item-subtitle">销量: 23台 | 销售额: ¥68,977</div>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 12px; color: #28a745;">+22.1%</div>
                            </div>
                        </div>
                        <div class="list-item">
                            <div class="list-item-icon accent-icon">
                                <span style="font-weight: bold; color: white;">4</span>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">蓝牙耳机</div>
                                <div class="list-item-subtitle">销量: 67个 | 销售额: ¥13,333</div>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 12px; color: #28a745;">+5.3%</div>
                            </div>
                        </div>
                        <div class="list-item">
                            <div class="list-item-icon accent-icon">
                                <span style="font-weight: bold; color: white;">5</span>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">护肤套装</div>
                                <div class="list-item-subtitle">销量: 45套 | 销售额: ¥17,955</div>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 12px; color: #dc3545;">-2.8%</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="card">
                        <div class="card-header">
                            <div class="card-title">销售渠道分析</div>
                        </div>
                        <div style="padding: 15px 0;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                                <div>
                                    <div style="font-weight: 500;">线上商城</div>
                                    <div style="font-size: 12px; color: #666;">65% 的销售额</div>
                                </div>
                                <div style="text-align: right;">
                                    <div style="font-weight: 600; color: var(--accent);">¥29,691</div>
                                </div>
                            </div>
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                                <div>
                                    <div style="font-weight: 500;">移动端APP</div>
                                    <div style="font-size: 12px; color: #666;">25% 的销售额</div>
                                </div>
                                <div style="text-align: right;">
                                    <div style="font-weight: 600; color: var(--accent);">¥11,420</div>
                                </div>
                            </div>
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <div style="font-weight: 500;">线下门店</div>
                                    <div style="font-size: 12px; color: #666;">10% 的销售额</div>
                                </div>
                                <div style="text-align: right;">
                                    <div style="font-weight: 600; color: var(--accent);">¥4,567</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `
    },
    
    'user-analytics': {
        title: '用户分析',
        subtitle: '用户行为数据分析',
        content: `
            <div class="mobile-page">
                <div class="mobile-header">
                    <h1>用户分析</h1>
                    <div class="subtitle">用户行为数据分析</div>
                </div>
                <div class="mobile-content">
                    <div class="card">
                        <div class="card-header">
                            <div class="card-title">时间筛选</div>
                        </div>
                        <div style="display: flex; gap: 10px; margin-bottom: 15px;">
                            <button class="btn btn-secondary" style="flex: 1; font-size: 14px; padding: 8px 12px;" onclick="filterUsers('today')">今日</button>
                            <button class="btn btn-secondary" style="flex: 1; font-size: 14px; padding: 8px 12px;" onclick="filterUsers('week')">本周</button>
                            <button class="btn" style="flex: 1; font-size: 14px; padding: 8px 12px;" onclick="filterUsers('month')">本月</button>
                            <button class="btn btn-secondary" style="flex: 1; font-size: 14px; padding: 8px 12px;" onclick="filterUsers('year')">本年</button>
                        </div>
                    </div>
                    
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-number">1,234</div>
                            <div class="stat-label">总用户数</div>
                            <div style="font-size: 12px; color: #28a745; margin-top: 5px;">↗ +5.2%</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">567</div>
                            <div class="stat-label">活跃用户</div>
                            <div style="font-size: 12px; color: #28a745; margin-top: 5px;">↗ +8.7%</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">89.2%</div>
                            <div class="stat-label">用户留存率</div>
                            <div style="font-size: 12px; color: #28a745; margin-top: 5px;">↗ +2.3%</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">4.5h</div>
                            <div class="stat-label">平均使用时长</div>
                            <div style="font-size: 12px; color: #dc3545; margin-top: 5px;">↘ -0.8%</div>
                        </div>
                    </div>
                    
                    <div class="card">
                        <div class="card-header">
                            <div class="card-title">用户增长趋势</div>
                        </div>
                        <div class="chart-placeholder">
                            <div style="text-align: center;">
                                <i class="fas fa-chart-area chart-placeholder-icon"></i>
                                <div style="font-weight: 500;">用户增长趋势图</div>
                                <div style="font-size: 12px; margin-top: 5px; color: var(--text-muted);">（演示用图表占位）</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="card">
                        <div class="card-header">
                            <div class="card-title">用户年龄分布</div>
                        </div>
                        <div style="padding: 15px 0;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                                <div>
                                    <div style="font-weight: 500;">18-25岁</div>
                                    <div style="font-size: 12px; color: #666;">35% 的用户</div>
                                </div>
                                <div style="text-align: right;">
                                    <div style="font-weight: 600; color: var(--accent);">432人</div>
                                </div>
                            </div>
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                                <div>
                                    <div style="font-weight: 500;">26-35岁</div>
                                    <div style="font-size: 12px; color: #666;">28% 的用户</div>
                                </div>
                                <div style="text-align: right;">
                                    <div style="font-weight: 600; color: var(--accent);">346人</div>
                                </div>
                            </div>
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                                <div>
                                    <div style="font-weight: 500;">36-45岁</div>
                                    <div style="font-size: 12px; color: #666;">22% 的用户</div>
                                </div>
                                <div style="text-align: right;">
                                    <div style="font-weight: 600; color: var(--accent);">271人</div>
                                </div>
                            </div>
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <div style="font-weight: 500;">46岁以上</div>
                                    <div style="font-size: 12px; color: #666;">15% 的用户</div>
                                </div>
                                <div style="text-align: right;">
                                    <div style="font-weight: 600; color: var(--accent);">185人</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="card">
                        <div class="card-header">
                            <div class="card-title">用户地域分布 TOP5</div>
                        </div>
                        <div class="list-item">
                            <div class="list-item-icon" style="background: #ffd700;">
                                <span style="font-weight: bold; color: white;">1</span>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">北京</div>
                                <div class="list-item-subtitle">用户数: 234人 (19%)</div>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 12px; color: #28a745;">+12.5%</div>
                            </div>
                        </div>
                        <div class="list-item">
                            <div class="list-item-icon" style="background: #c0c0c0;">
                                <span style="font-weight: bold; color: white;">2</span>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">上海</div>
                                <div class="list-item-subtitle">用户数: 189人 (15%)</div>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 12px; color: #28a745;">+8.3%</div>
                            </div>
                        </div>
                        <div class="list-item">
                            <div class="list-item-icon" style="background: #cd7f32;">
                                <span style="font-weight: bold; color: white;">3</span>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">广州</div>
                                <div class="list-item-subtitle">用户数: 156人 (13%)</div>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 12px; color: #28a745;">+6.7%</div>
                            </div>
                        </div>
                        <div class="list-item">
                            <div class="list-item-icon accent-icon">
                                <span style="font-weight: bold; color: white;">4</span>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">深圳</div>
                                <div class="list-item-subtitle">用户数: 145人 (12%)</div>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 12px; color: #28a745;">+4.2%</div>
                            </div>
                        </div>
                        <div class="list-item">
                            <div class="list-item-icon accent-icon">
                                <span style="font-weight: bold; color: white;">5</span>
                            </div>
                            <div class="list-item-content">
                                <div class="list-item-title">杭州</div>
                                <div class="list-item-subtitle">用户数: 98人 (8%)</div>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 12px; color: #28a745;">+15.8%</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="card">
                        <div class="card-header">
                            <div class="card-title">用户行为分析</div>
                        </div>
                        <div style="padding: 15px 0;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                                <div>
                                    <div style="font-weight: 500;">平均访问时长</div>
                                    <div style="font-size: 12px; color: #666;">每次访问停留时间</div>
                                </div>
                                <div style="text-align: right;">
                                    <div style="font-weight: 600; color: var(--accent);">3.2分钟</div>
                                </div>
                            </div>
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                                <div>
                                    <div style="font-weight: 500;">页面跳出率</div>
                                    <div style="font-size: 12px; color: #666;">单页访问比例</div>
                                </div>
                                <div style="text-align: right;">
                                    <div style="font-weight: 600; color: #dc3545;">23.5%</div>
                                </div>
                            </div>
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                                <div>
                                    <div style="font-weight: 500;">转化率</div>
                                    <div style="font-size: 12px; color: #666;">访问到购买转化</div>
                                </div>
                                <div style="text-align: right;">
                                    <div style="font-weight: 600; color: #28a745;">8.7%</div>
                                </div>
                            </div>
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <div style="font-weight: 500;">复购率</div>
                                    <div style="font-size: 12px; color: #666;">重复购买用户比例</div>
                                </div>
                                <div style="text-align: right;">
                                    <div style="font-weight: 600; color: #28a745;">45.3%</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `
    }
};

// 当前页面
let currentPage = 'home';

// 商品详情数据
const productDetails = {
    '时尚T恤': {
        icon: 'fa-tshirt',
        price: '¥89',
        category: '服装',
        stock: '156件',
        status: '上架中',
        desc: '纯棉面料，透气舒适，简约百搭款式，适合日常休闲穿搭。',
        specs: { '颜色': '白色/黑色', '尺寸': 'S-XXL', '材质': '100%棉', '销量': '328件' }
    },
    '运动鞋': {
        icon: 'fa-shoe-prints',
        price: '¥299',
        category: '鞋类',
        stock: '89双',
        status: '上架中',
        desc: '轻便缓震跑鞋，透气网面设计，适合日常运动和休闲穿着。',
        specs: { '颜色': '黑白/灰蓝', '尺码': '36-44', '材质': '网面+橡胶', '销量': '156双' }
    },
    '智能手机': {
        icon: 'fa-mobile-alt',
        price: '¥2999',
        category: '数码',
        stock: '23台',
        status: '上架中',
        desc: '6.7英寸高清大屏，旗舰芯片，超长续航，支持快充与无线充电。',
        specs: { '存储': '256GB', '颜色': '深空灰', '屏幕': '6.7英寸', '销量': '45台' }
    },
    '笔记本电脑': {
        icon: 'fa-laptop',
        price: '¥5999',
        category: '数码',
        stock: '12台',
        status: '上架中',
        desc: '轻薄高性能笔记本，适合办公与创作，续航可达12小时。',
        specs: { '处理器': 'i7', '内存': '16GB', '硬盘': '512GB SSD', '销量': '18台' }
    },
    '蓝牙耳机': {
        icon: 'fa-headphones',
        price: '¥199',
        category: '数码',
        stock: '67个',
        status: '上架中',
        desc: '主动降噪，高清音质，30小时超长续航，支持触控操作。',
        specs: { '颜色': '白色', '续航': '30小时', '降噪': '主动降噪', '销量': '210个' }
    },
    '护肤套装': {
        icon: 'fa-spa',
        price: '¥399',
        category: '美妆',
        stock: '45套',
        status: '上架中',
        desc: '补水保湿护肤三件套，温和不刺激，适合多种肤质日常使用。',
        specs: { '规格': '水乳精华', '肤质': '所有肤质', '功效': '补水保湿', '销量': '89套' }
    },
    '咖啡机': {
        icon: 'fa-coffee',
        price: '¥1299',
        category: '家居',
        stock: '18台',
        status: '上架中',
        desc: '全自动意式咖啡机，一键萃取，自带奶泡系统，在家享受咖啡馆品质。',
        specs: { '容量': '1.5L', '功率': '1450W', '压力': '15Bar', '销量': '32台' }
    },
    '运动手表': {
        icon: 'fa-clock',
        price: '¥899',
        category: '数码',
        stock: '34个',
        status: '上架中',
        desc: '多功能运动手表，支持心率监测、GPS定位、50米防水。',
        specs: { '颜色': '黑色', '续航': '14天', '防水': '50米', '销量': '76个' }
    }
};

// 底部 Tab 与页面映射（子页面高亮对应主 Tab）
const tabPageMap = {
    home: 'home',
    profile: 'profile',
    settings: 'profile',
    products: 'products',
    'product-list': 'products',
    'product-add': 'products',
    orders: 'orders',
    'order-list': 'orders',
    'order-detail': 'orders',
    analytics: 'analytics',
    'sales-chart': 'analytics',
    'user-analytics': 'analytics'
};

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    // 加载首页
    loadPage('home');
    
    // 绑定导航事件
    bindNavigationEvents();
    
    // 绑定侧边栏切换事件
    bindSidebarToggle();

    // 小程序胶囊与状态栏
    bindMiniProgramChrome();

    // 底部 Tab 导航
    bindTabBarEvents();

    // 手机壳内弹窗
    bindPhoneModal();

    // 主题切换
    bindThemeToggle();
    syncThemeToggleUI(document.documentElement.getAttribute('data-theme') || 'dark');
});

// 主题切换
function bindThemeToggle() {
    const toggle = document.getElementById('themeToggle');
    if (!toggle) return;

    toggle.querySelectorAll('.theme-toggle-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const theme = this.getAttribute('data-theme');
            setTheme(theme);
        });
    });
}

function setTheme(theme) {
    if (theme !== 'light' && theme !== 'dark') return;
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('prototype-theme', theme);
    syncThemeToggleUI(theme);
}

function syncThemeToggleUI(theme) {
    document.querySelectorAll('.theme-toggle-btn').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-theme') === theme);
    });
}

// 小程序顶部栏交互
function bindMiniProgramChrome() {
    const timeEl = document.querySelector('.mp-time');
    if (timeEl) {
        const updateTime = () => {
            const now = new Date();
            timeEl.textContent = `${now.getHours()}:${String(now.getMinutes()).padStart(2, '0')}`;
        };
        updateTime();
        setInterval(updateTime, 30000);
    }

    const moreBtn = document.querySelector('.mp-capsule-more');
    const closeBtn = document.querySelector('.mp-capsule-close');

    if (moreBtn) {
        moreBtn.addEventListener('click', () => {
            alert('小程序菜单\n\n- 转发给朋友\n- 添加到我的小程序\n- 设置\n- 反馈与投诉');
        });
    }

    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            alert('关闭小程序\n\n将返回微信聊天界面');
        });
    }
}

// 底部 Tab 导航事件
function bindTabBarEvents() {
    document.querySelectorAll('.mp-tabbar-item').forEach(item => {
        item.addEventListener('click', function() {
            const page = this.getAttribute('data-page');
            if (page) {
                loadPage(page);
            }
        });
    });
}

// 更新底部 Tab 高亮状态
function updateTabBarState(pageName) {
    const activeTab = tabPageMap[pageName] || pageName;
    document.querySelectorAll('.mp-tabbar-item').forEach(item => {
        item.classList.toggle('active', item.getAttribute('data-page') === activeTab);
    });
}

// 绑定导航事件
function bindNavigationEvents() {
    // 主菜单项点击事件
    document.querySelectorAll('.nav-item.main-item').forEach(item => {
        item.addEventListener('click', function() {
            const page = this.getAttribute('data-page');
            
            // 如果有子菜单，切换展开状态
            const subMenu = this.nextElementSibling;
            if (subMenu && subMenu.classList.contains('sub-menu')) {
                this.classList.toggle('expanded');
                subMenu.classList.toggle('expanded');
            } else {
                // 没有子菜单，直接加载页面
                loadPage(page);
            }
        });
    });
    
    // 子菜单项点击事件
    document.querySelectorAll('.nav-item.sub-item').forEach(item => {
        item.addEventListener('click', function() {
            const page = this.getAttribute('data-page');
            loadPage(page);
        });
    });
}

// 绑定侧边栏切换事件
function bindSidebarToggle() {
    const toggleBtn = document.getElementById('toggleBtn');
    const sidebar = document.getElementById('sidebar');
    
    toggleBtn.addEventListener('click', function() {
        sidebar.classList.toggle('collapsed');
        
        // 更新按钮图标
        const icon = this.querySelector('i');
        if (sidebar.classList.contains('collapsed')) {
            icon.className = 'fas fa-chevron-right';
        } else {
            icon.className = 'fas fa-bars';
        }
    });
}

// 加载页面
function loadPage(pageName) {
    const phoneContent = document.getElementById('phoneContent');
    const pageInfo = pageData[pageName];
    
    if (pageInfo) {
        // 切换页面时关闭弹窗
        closePhoneModal();

        // 更新页面内容
        phoneContent.innerHTML = pageInfo.content;
        
        // 更新当前页面
        currentPage = pageName;
        
        // 更新导航状态
        updateNavigationState(pageName);

        // 更新底部 Tab 状态
        updateTabBarState(pageName);
        
        // 滚动到顶部
        phoneContent.scrollTop = 0;

        // 同步小程序顶栏样式（渐变页用浅色状态栏文字）
        updateMiniProgramChrome(pageName);
    }
}

// 根据页面调整小程序顶栏配色
function updateMiniProgramChrome(pageName) {
    const chrome = document.querySelector('.mp-chrome');
    if (!chrome) return;

    const gradientPages = Object.keys(pageData);
    if (gradientPages.includes(pageName)) {
        chrome.classList.remove('mp-chrome--light');
    } else {
        chrome.classList.add('mp-chrome--light');
    }
}

// 更新导航状态
function updateNavigationState(pageName) {
    // 清除所有活动状态
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // 设置当前页面的活动状态
    const activeItem = document.querySelector(`[data-page="${pageName}"]`);
    if (activeItem) {
        activeItem.classList.add('active');
        
        // 如果是子菜单项，展开父菜单
        if (activeItem.classList.contains('sub-item')) {
            const parentSection = activeItem.closest('.nav-section');
            const mainItem = parentSection.querySelector('.main-item');
            const subMenu = parentSection.querySelector('.sub-menu');
            
            if (mainItem && subMenu) {
                mainItem.classList.add('expanded');
                subMenu.classList.add('expanded');
            }
        }
    }
}

// 全局页面加载函数（供HTML中的onclick调用）
window.loadPage = loadPage;

// 手机壳内弹窗控制
function bindPhoneModal() {
    const mask = document.getElementById('phoneModalMask');
    const closeBtn = document.getElementById('phoneModalClose');

    if (mask) mask.addEventListener('click', closePhoneModal);
    if (closeBtn) closeBtn.addEventListener('click', closePhoneModal);

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closePhoneModal();
    });
}

function openPhoneModal(html) {
    const modal = document.getElementById('phoneModal');
    const body = document.getElementById('phoneModalBody');
    if (!modal || !body) return;

    body.innerHTML = html;
    modal.classList.add('is-open');
    modal.setAttribute('aria-hidden', 'false');
}

function closePhoneModal() {
    const modal = document.getElementById('phoneModal');
    if (!modal) return;

    modal.classList.remove('is-open');
    modal.setAttribute('aria-hidden', 'true');
}

// 商品详情展示（手机壳内底部弹窗）
function showProductDetail(productName) {
    const product = productDetails[productName];
    if (!product) return;

    const specsHtml = Object.entries(product.specs).map(([key, val]) => `
        <div class="product-detail-spec">
            <label>${key}</label>
            <span>${val}</span>
        </div>
    `).join('');

    const html = `
        <div class="product-detail-hero">
            <div class="product-detail-icon">
                <i class="fas ${product.icon}"></i>
            </div>
            <div class="product-detail-meta">
                <h2>${productName}</h2>
                <div class="product-detail-price">${product.price}</div>
                <div class="product-detail-tags">
                    <span class="product-detail-tag">${product.category}</span>
                    <span class="product-detail-tag status-on">${product.status}</span>
                </div>
            </div>
        </div>
        <div class="product-detail-section">
            <h3>库存状态</h3>
            <p>当前库存 <strong>${product.stock}</strong>，销售情况良好。</p>
        </div>
        <div class="product-detail-section">
            <h3>商品描述</h3>
            <p>${product.desc}</p>
        </div>
        <div class="product-detail-section">
            <h3>规格参数</h3>
            <div class="product-detail-specs">${specsHtml}</div>
        </div>
        <div class="product-detail-actions">
            <button class="btn btn-secondary" type="button" onclick="closePhoneModal()">关闭</button>
            <button class="btn" type="button" onclick="closePhoneModal()">编辑商品</button>
        </div>
    `;

    openPhoneModal(html);
}

window.showProductDetail = showProductDetail;
window.closePhoneModal = closePhoneModal;

// 图片上传函数
function uploadImage() {
    alert('图片上传功能\n\n在实际应用中，这里会：\n- 打开文件选择器\n- 上传图片到服务器\n- 显示上传进度\n- 预览上传的图片');
}

// 表单重置函数
function resetForm() {
    document.getElementById('productName').value = '';
    document.getElementById('productCategory').value = '';
    document.getElementById('productPrice').value = '';
    document.getElementById('productStock').value = '';
    document.getElementById('productSpec').value = '';
    document.getElementById('productDesc').value = '';
    document.querySelector('input[name="status"][value="active"]').checked = true;
    alert('表单已重置');
}

// 提交商品函数
function submitProduct() {
    const name = document.getElementById('productName').value;
    const category = document.getElementById('productCategory').value;
    const price = document.getElementById('productPrice').value;
    const stock = document.getElementById('productStock').value;
    
    if (!name || !category || !price || !stock) {
        alert('请填写所有必填字段');
        return;
    }
    
    alert('商品创建成功！\n\n商品名称：' + name + '\n分类：' + category + '\n价格：¥' + price + '\n库存：' + stock + '件');
    loadPage('product-list');
}

// 订单筛选函数
function filterOrders(status) {
    const buttons = document.querySelectorAll('[onclick^="filterOrders"]');
    buttons.forEach(btn => {
        btn.className = 'btn btn-secondary';
    });
    event.target.className = 'btn';
    
    alert('筛选订单状态：' + status + '\n\n在实际应用中，这里会：\n- 根据状态筛选订单列表\n- 更新页面显示\n- 保持筛选状态');
}

// 联系客服函数
function contactCustomer() {
    alert('联系客服\n\n客服电话：400-123-4567\n客服微信：kefu123\n在线客服：9:00-21:00');
}

// 更新订单状态函数
function updateOrderStatus() {
    alert('更新订单状态\n\n可选择的操作：\n- 确认发货\n- 标记完成\n- 取消订单\n- 申请退款');
}

// 销售数据筛选函数
function filterSales(period) {
    const buttons = document.querySelectorAll('[onclick^="filterSales"]');
    buttons.forEach(btn => {
        btn.className = 'btn btn-secondary';
    });
    event.target.className = 'btn';
    
    alert('筛选销售数据：' + period + '\n\n在实际应用中，这里会：\n- 根据时间范围更新数据\n- 重新计算统计指标\n- 更新图表显示');
}

// 用户数据筛选函数
function filterUsers(period) {
    const buttons = document.querySelectorAll('[onclick^="filterUsers"]');
    buttons.forEach(btn => {
        btn.className = 'btn btn-secondary';
    });
    event.target.className = 'btn';
    
    alert('筛选用户数据：' + period + '\n\n在实际应用中，这里会：\n- 根据时间范围更新用户数据\n- 重新计算用户指标\n- 更新分析图表');
} 