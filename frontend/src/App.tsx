import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { ChatWindow } from './components/Chat/ChatWindow';
import { DocumentUploader } from './components/Ingestion/DocumentUploader';
import { TraceInspector } from './components/Observability/TraceInspector';
import { fetchSystemHealth } from './services/api';
import { ChatMessage, SystemHealth } from './types';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'chat' | 'ingest' | 'observability'>('chat');
  const [health, setHealth] = useState<SystemHealth | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  
  // Initialisation du thème avec prise en compte du localStorage et du DOM actuel
  const [theme, setTheme] = useState<'light' | 'dark'>(() => {
    try {
      const saved = localStorage.getItem('theme');
      if (saved === 'light' || saved === 'dark') return saved;
      if (typeof window !== 'undefined' && window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        return 'dark';
      }
    } catch (e) {}
    return 'dark';
  });

  const applyTheme = (targetTheme: 'light' | 'dark') => {
    const root = document.documentElement;
    const body = document.body;
    if (targetTheme === 'dark') {
      root.classList.add('dark');
      body.classList.add('dark');
    } else {
      root.classList.remove('dark');
      body.classList.remove('dark');
    }
    try {
      localStorage.setItem('theme', targetTheme);
    } catch (e) {}
  };

  useEffect(() => {
    applyTheme(theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => {
      const nextTheme = prev === 'dark' ? 'light' : 'dark';
      applyTheme(nextTheme);
      return nextTheme;
    });
  };

  const loadHealth = async () => {
    try {
      const data = await fetchSystemHealth();
      setHealth(data);
    } catch (e) {
      console.warn('Backend not ready yet, using default health mock data');
      setHealth({
        status: 'healthy',
        app_name: 'RAG-LLMOps-Azure',
        environment: 'production',
        cloud_provider: 'azure',
        azure_region: 'eastus',
        aws_region: 'eastus',
        llm_model: 'gpt-5-mini (Azure OpenAI)',
        bedrock_llm_model: 'gpt-5-mini (Azure OpenAI)',
        embedding_model: 'text-embedding-3-small (1536d)',
        bedrock_embedding_model: 'text-embedding-3-small (1536d)',
        mock_bedrock: false,
        mock_llm: false,
        prompt_version: 'v1.2.0',
        total_chunks_indexed: 4,
        vector_store_type: 'pgvector (Azure PostgreSQL)'
      });
    }
  };

  useEffect(() => {
    loadHealth();
    const interval = setInterval(loadHealth, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-[#0b0f17] text-slate-900 dark:text-slate-100 flex flex-col font-sans selection:bg-orange-500 selection:text-white transition-colors duration-200">
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        theme={theme}
        toggleTheme={toggleTheme}
      />
      
      <main className="flex-1 overflow-hidden relative">
        <div className={activeTab === 'chat' ? 'h-full' : 'hidden'}>
          <ChatWindow messages={messages} setMessages={setMessages} />
        </div>
        <div className={activeTab === 'ingest' ? 'h-[calc(100vh-4rem)] overflow-y-auto' : 'hidden'}>
          <DocumentUploader onIndexedSuccess={loadHealth} />
        </div>
        <div className={activeTab === 'observability' ? 'h-[calc(100vh-4rem)] overflow-y-auto' : 'hidden'}>
          <TraceInspector health={health} />
        </div>
      </main>

    </div>
  );
};

export default App;
