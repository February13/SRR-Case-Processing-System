"""
NLP增强处理器
使用transformer、BERT等技术进行智能文本总结和内容分析
"""

import re
import os
from typing import Optional, Dict, Any, List
import warnings
warnings.filterwarnings('ignore')

class NLPEnhancedProcessor:
    """NLP增强处理器"""
    
    def __init__(self):
        self.summarizer = None
        self._init_nlp_models()
    
    def _init_nlp_models(self):
        """初始化NLP模型"""
        # 直接使用规则基础方法，避免transformer模型的性能问题
        print("✅ 使用优化的规则基础NLP处理")
        self.summarizer = None
    
    def extract_nature_of_request(self, txt_content: str, email_content: str = None) -> str:
        """
        使用NLP技术提取和总结Nature of Request
        
        Args:
            txt_content (str): TXT文件内容
            email_content (str): 邮件内容（如果存在）
            
        Returns:
            str: 智能总结的诉求内容
        """
        # 优先使用邮件内容进行总结（如果存在）
        if email_content and email_content.strip():
            print("📧 优先使用邮件内容进行总结")
            email_summary = self._rule_based_summarize_email(email_content)
            if email_summary and email_summary.strip():
                print("✅ 邮件内容总结成功")
                return email_summary
        
        # 如果邮件内容无法总结，使用TXT内容
        source_content = txt_content if txt_content and txt_content.strip() else ""
        
        if not source_content.strip():
            return "无法提取诉求内容"
        
        print("🔍 使用优化的NLP技术分析诉求内容...")
        
        # 直接使用优化的规则基础方法（更快更准确）
        rule_summary = self._rule_based_summarize(source_content)
        if rule_summary and rule_summary.strip():
            print("✅ 优化规则总结成功")
            return rule_summary
        
        # 如果规则方法失败，尝试从邮件内容中提取
        if email_content and email_content.strip():
            email_summary = self._rule_based_summarize(email_content)
            if email_summary and email_summary.strip():
                print("✅ 邮件内容总结成功")
                return email_summary
        
        # 备选：使用关键词提取
        keyword_summary = self._keyword_based_summarize(source_content)
        if keyword_summary and keyword_summary.strip():
            print("✅ 关键词总结成功")
            return keyword_summary
        
        # 最后备选：简单文本截取
        if len(source_content) > 50:
            return source_content[:50] + "..."
        
        return "无法提取有效信息"
    
    def _transformer_summarize(self, content: str) -> Optional[str]:
        """使用transformer模型进行总结"""
        if not self.summarizer:
            return None
        
        try:
            # 清理和预处理文本
            cleaned_content = self._preprocess_text(content)
            
            # 限制输入长度（transformer模型有输入长度限制）
            max_length = 1000
            if len(cleaned_content) > max_length:
                cleaned_content = cleaned_content[:max_length]
            
            # 使用transformer模型总结
            summary = self.summarizer(cleaned_content, max_length=100, min_length=20, do_sample=False)
            
            if summary and len(summary) > 0:
                return summary[0]['summary_text']
            
        except Exception as e:
            print(f"Transformer总结异常: {e}")
        
        return None
    
    def _rule_based_summarize_email(self, email_content: str) -> Optional[str]:
        """
        专门处理邮件内容的总结方法
        """
        try:
            # 从邮件内容中提取关键信息
            summary_parts = []
            
            # 1. 提取案件编号
            case_match = re.search(r'<CASE>:\s*([^\n]+)', email_content)
            if case_match:
                case_no = case_match.group(1).strip()
                summary_parts.append(f"案件编号: {case_no}")
            
            # 2. 提取部门信息
            dept_match = re.search(r'<DEPT>:\s*([^\n]+)', email_content)
            if dept_match:
                dept = dept_match.group(1).strip()
                summary_parts.append(f"负责部门: {dept}")
            
            # 3. 提取收件人信息
            to_match = re.search(r'To:\s*-\s*([^\n,]+)', email_content)
            if to_match:
                to_dept = to_match.group(1).strip()
                summary_parts.append(f"转介至: {to_dept}")
            
            # 4. 识别查询类型
            if 'enquiry' in email_content.lower():
                summary_parts.append("查询请求")
            
            if 'referral' in email_content.lower():
                summary_parts.append("转介处理")
            
            # 5. 提取时间要求
            if '10 calendar days' in email_content:
                summary_parts.append("10天回复要求")
            
            if '21 calendar days' in email_content:
                summary_parts.append("21天最终回复要求")
            
            if summary_parts:
                return " | ".join(summary_parts)
            
        except Exception as e:
            print(f"邮件内容总结异常: {e}")
        
        return None
    
    def _rule_based_summarize(self, content: str) -> Optional[str]:
        """优化的规则基础总结方法"""
        try:
            # 快速提取关键信息
            summary_parts = []
            
            # 1. 提取主旨信息（最重要）
            subject_match = re.search(r'主旨[：:]\s*([^\n]+)', content)
            if subject_match:
                subject = subject_match.group(1).strip()
                # 截取关键部分，避免过长
                if len(subject) > 80:
                    subject = subject[:80] + "..."
                if '查詢' in subject and '斜坡' in subject:
                    summary_parts.append(f"查询斜坡维修进度: {subject}")
                elif '斜坡' in subject:
                    summary_parts.append(f"斜坡相关问题: {subject}")
                else:
                    summary_parts.append(f"主题: {subject}")
            
            # 1.1 提取Subject Matter信息
            subject_matter_match = re.search(r'Subject Matter[：:]\s*([^\n]+)', content)
            if subject_matter_match:
                subject_matter = subject_matter_match.group(1).strip()
                summary_parts.append(f"事项: {subject_matter}")
            
            # 1.2 提取Description信息
            desc_match = re.search(r'Description[：:]\s*([^\n]+)', content)
            if desc_match:
                description = desc_match.group(1).strip()
                summary_parts.append(f"描述: {description}")
            
            # 2. 提取请求类型
            request_match = re.search(r'Request Type[：:]\s*([^\n]+)', content)
            if request_match:
                request_type = request_match.group(1).strip()
                summary_parts.append(f"请求类型: {request_type}")
            
            # 3. 提取斜坡编号
            slope_match = re.search(r'斜坡編號([^\s]+)|11SW[-\w/]+', content)
            if slope_match:
                slope = slope_match.group(0).strip()
                summary_parts.append(f"涉及斜坡: {slope}")
            
            # 4. 提取主要关注点
            if '進度' in content:
                summary_parts.append("关注工程进度")
            elif '維修' in content:
                summary_parts.append("关注维修情况")
            elif '查詢' in content:
                summary_parts.append("查询请求")
            
            # 5. 构建最终总结
            if summary_parts:
                return " | ".join(summary_parts)
            
            # 6. 如果没有找到关键信息，提取关键句子
            lines = content.split('\\n')
            key_lines = []
            for line in lines:
                line = line.strip()
                if len(line) > 10 and any(keyword in line for keyword in ['查詢', '斜坡', '維修', '進度', '11SW']):
                    # 截取关键部分，避免过长
                    if len(line) > 100:
                        line = line[:100] + "..."
                    key_lines.append(line)
                    if len(key_lines) >= 2:  # 最多取2行
                        break
            
            if key_lines:
                return " | ".join(key_lines)
            
            # 7. 最后备选：简单文本截取
            if len(content) > 100:
                return content[:100] + "..."
            
        except Exception as e:
            print(f"规则基础总结异常: {e}")
        
        return None
    
    def _keyword_based_summarize(self, content: str) -> Optional[str]:
        """基于关键词的总结方法"""
        try:
            # 提取关键词和短语
            keywords = self._extract_keywords(content)
            
            if keywords:
                # 构建关键词总结
                return f"关键词总结: {', '.join(keywords[:5])}"
            
        except Exception as e:
            print(f"关键词总结异常: {e}")
        
        return None
    
    def _preprocess_text(self, content: str) -> str:
        """预处理文本"""
        # 移除多余空白
        content = re.sub(r'\s+', ' ', content)
        
        # 移除特殊字符
        content = re.sub(r'[^\w\s\u4e00-\u9fff.,!?]', ' ', content)
        
        # 移除过短的行
        lines = content.split('\n')
        filtered_lines = [line.strip() for line in lines if len(line.strip()) > 10]
        
        return ' '.join(filtered_lines)
    
    def _extract_key_information(self, content: str) -> Dict[str, str]:
        """提取关键信息 - 专注于实际诉求内容"""
        key_info = {}
        
        # 提取主题 - 专注于实际诉求
        subject_patterns = [
            r'主旨[：:]\s*([^\n]+)',
            r'Subject Matter[：:]\s*([^\n]+)',
            r'查詢斜坡維修編號([^\n]+)維修工程進度',
            r'斜坡事項[^\n]*',
            r'查詢[^\n]*斜坡[^\n]*',
        ]
        
        for pattern in subject_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                subject = match.group(1).strip() if match.groups() else match.group(0).strip()
                key_info['subject'] = subject
                break
        
        # 提取请求类型
        request_patterns = [
            r'Request Type[：:]\s*([^\n]+)',
            r'請求類型[：:]\s*([^\n]+)',
        ]
        
        for pattern in request_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                key_info['request_type'] = match.group(1).strip()
                break
        
        # 提取斜坡信息 - 更精确的匹配
        slope_patterns = [
            r'斜坡編號([^\s]+)',
            r'11SW[-\w/]+',
            r'維修編號([^\s]+)',
            r'斜坡[^\n]*編號[^\n]*',
        ]
        
        for pattern in slope_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                slope = match.group(1).strip() if match.groups() else match.group(0).strip()
                key_info['slope_info'] = slope
                break
        
        # 提取主要关注点 - 专注于实际诉求
        concern_patterns = [
            r'查詢[^\n]*進度[^\n]*',
            r'維修[^\n]*進度[^\n]*',
            r'工程[^\n]*進度[^\n]*',
            r'斜坡[^\n]*維修[^\n]*',
            r'查詢人[^\n]*斜坡[^\n]*',
        ]
        
        for pattern in concern_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                key_info['main_concern'] = match.group(0).strip()
                break
        
        # 提取描述信息
        description_patterns = [
            r'Description[：:]\s*([^\n]+)',
            r'查詢人提供斜坡編號為([^\n]+)',
            r'斜坡屬([^\n]+)負責',
        ]
        
        for pattern in description_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                key_info['description'] = match.group(1).strip() if match.groups() else match.group(0).strip()
                break
        
        return key_info
    
    def _extract_keywords(self, content: str) -> List[str]:
        """提取关键词"""
        keywords = []
        
        # 定义关键词模式
        keyword_patterns = [
            r'斜坡[^\s]*',
            r'維修[^\s]*',
            r'工程[^\s]*',
            r'進度[^\s]*',
            r'查詢[^\s]*',
            r'11SW[^\s]*',
            r'編號[^\s]*',
        ]
        
        for pattern in keyword_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            keywords.extend(matches)
        
        # 去重并限制数量
        unique_keywords = list(set(keywords))
        return unique_keywords[:10]
    
    def analyze_email_content(self, email_content: str) -> str:
        """分析邮件内容"""
        if not email_content or not email_content.strip():
            return "无邮件内容"
        
        # 提取邮件中的关键信息
        email_info = self._extract_email_information(email_content)
        
        if email_info:
            return f"邮件内容: {email_info}"
        
        return "邮件内容分析完成"
    
    def _extract_email_information(self, email_content: str) -> Optional[str]:
        """提取邮件信息"""
        # 查找邮件中的关键信息
        patterns = [
            r'查詢[^\n]*斜坡[^\n]*',
            r'斜坡[^\n]*維修[^\n]*',
            r'工程[^\n]*進度[^\n]*',
            r'11SW[^\n]*',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, email_content, re.IGNORECASE)
            if match:
                return match.group(0).strip()
        
        return None


# 全局处理器实例
_nlp_processor = None

def get_nlp_enhanced_nature_of_request(txt_content: str, email_content: str = None) -> str:
    """
    获取NLP增强的Nature of Request（全局函数）
    
    Args:
        txt_content (str): TXT文件内容
        email_content (str): 邮件内容（如果存在）
        
    Returns:
        str: 智能总结的诉求内容
    """
    global _nlp_processor
    
    if _nlp_processor is None:
        _nlp_processor = NLPEnhancedProcessor()
    
    return _nlp_processor.extract_nature_of_request(txt_content, email_content)


def analyze_email_content(email_content: str) -> str:
    """
    分析邮件内容（全局函数）
    
    Args:
        email_content (str): 邮件内容
        
    Returns:
        str: 分析结果
    """
    global _nlp_processor
    
    if _nlp_processor is None:
        _nlp_processor = NLPEnhancedProcessor()
    
    return _nlp_processor.analyze_email_content(email_content)


if __name__ == "__main__":
    # 测试NLP增强处理器
    print("=" * 70)
    print("NLP增强处理器测试")
    print("=" * 70)
    
    # 测试TXT文件
    txt_file = "exampleInput/txt/3-3YXXSJV.txt"
    email_file = "exampleInput/txt/emailcontent_3-3YXXSJV.txt"
    
    if os.path.exists(txt_file):
        print(f"\\n测试TXT文件: {txt_file}")
        with open(txt_file, 'r', encoding='utf-8') as f:
            txt_content = f.read()
        
        email_content = None
        if os.path.exists(email_file):
            print(f"测试邮件文件: {email_file}")
            with open(email_file, 'r', encoding='utf-8') as f:
                email_content = f.read()
        
        # 使用NLP增强处理
        nature_of_request = get_nlp_enhanced_nature_of_request(txt_content, email_content)
        print(f"\\nNLP增强总结结果:")
        print(f"Nature of Request: {nature_of_request}")
    else:
        print("测试文件不存在")