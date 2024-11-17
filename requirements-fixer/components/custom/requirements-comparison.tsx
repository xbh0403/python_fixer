"use client";

import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Loader2, Copy, Check } from 'lucide-react';

const RequirementsComparison: React.FC = () => {
  const [githubUrl, setGithubUrl] = useState('');
  const [errorMsg, setErrorMsg] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [copied, setCopied] = useState(false);
  const [originalReqs, setOriginalReqs] = useState('');
  const [fixedReqs, setFixedReqs] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setErrorMsg('');
    
    try {
      const response = await fetch('http://localhost:8000/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url: githubUrl,
          file_path: 'requirements.txt'
        }),
      });
  
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to process repository');
      }
  
      const data = await response.json();
      setOriginalReqs(data.original_requirements);
      setFixedReqs(data.fixed_requirements);
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to process repository';
      setErrorMsg(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(fixedReqs);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      setErrorMsg('Failed to copy to clipboard');
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <Card className="mb-8">
        <CardHeader>
          <CardTitle className="text-center text-3xl font-bold">
            Requirements.txt Fixer
          </CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <Input
              placeholder="Enter GitHub repository URL"
              value={githubUrl}
              onChange={(e) => setGithubUrl(e.target.value)}
              className="w-full"
            />
            <Button 
              type="submit" 
              className="w-full"
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Processing
                </>
              ) : (
                'Fix Requirements'
              )}
            </Button>
          </form>
        </CardContent>
      </Card>

      {errorMsg && (
        <Alert variant="destructive" className="mb-4">
          <AlertDescription>{errorMsg}</AlertDescription>
        </Alert>
      )}

      {(originalReqs || fixedReqs) && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Card>
            <CardHeader>
              <CardTitle>Original Requirements</CardTitle>
            </CardHeader>
            <CardContent>
              <pre className="bg-secondary p-4 rounded-lg overflow-auto">
                <code>{originalReqs}</code>
              </pre>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex justify-between items-center">
                Fixed Requirements
                <Button
                  variant="outline"
                  size="icon"
                  onClick={copyToClipboard}
                  className="h-8 w-8"
                >
                  {copied ? (
                    <Check className="h-4 w-4" />
                  ) : (
                    <Copy className="h-4 w-4" />
                  )}
                </Button>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <pre className="bg-secondary p-4 rounded-lg overflow-auto">
                <code>{fixedReqs}</code>
              </pre>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};

export default RequirementsComparison;