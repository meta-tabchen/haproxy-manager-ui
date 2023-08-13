from haproxy_manager import HAProxy


# 初始化 HAProxy 对象
haproxy_config = HAProxy()

# 更新后端配置
haproxy_config.update_backend("test", "test.tal-tb.com", 5000, "127.0.0.1")

# 将更改保存到 HAProxy 配置文件中
haproxy_config.save_to_file()
# haproxy_config.restart()

# 如果您决定删除后端配置：
# haproxy_config.delete_backend("test", "test.tal-tb.com")
# haproxy_config.save_to_file()
