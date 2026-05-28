'use client';

import React, { useState, useCallback, useRef, useEffect } from 'react';
import { useTranslations } from 'next-intl';
import { FileUploader } from '../FileUploader';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';

export interface StampsToolProps {
  className?: string;
}

interface StampState {
  file: File | null;
  blobUrl: string | null;
  viewerReady: boolean;
}

export function StampsTool({ className = '' }: StampsToolProps) {
  const t = useTranslations('common');
  const tTools = useTranslations('tools.stamps');

  const [stampState, setStampState] = useState<StampState>({
    file: null,
    blobUrl: null,
    viewerReady: false,
  });
  const [error, setError] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const iframeRef = useRef<HTMLIFrameElement>(null);

  useEffect(() => {
    return () => {
      if (stampState.blobUrl) URL.revokeObjectURL(stampState.blobUrl);
    };
  }, [stampState.blobUrl]);

  const handleFilesSelected = useCallback((files: File[]) => {
    if (files.length > 0) {
      const file = files[0];
      if (stampState.blobUrl) URL.revokeObjectURL(stampState.blobUrl);
      const blobUrl = URL.createObjectURL(file);
      setStampState({ file, blobUrl, viewerReady: false });
      setError(null);
    }
  }, [stampState.blobUrl]);

  const handleUploadError = useCallback((msg: string) => setError(msg), []);

  const handleIframeLoad = useCallback(() => {
    setTimeout(() => setStampState(prev => ({ ...prev, viewerReady: true })), 1500);
  }, []);

  // Note: we intentionally do NOT provide our own "Save" button. The annotation
  // viewer's built-in Export button (in its toolbar) is the only path that
  // includes the stamps — they live in the extension's own Konva-based store
  // (painter.getData()), NOT in PDF.js's annotationStorage, so
  // pdfDocument.saveDocument() would silently drop them. Matches EditPDFTool's
  // pattern of relying on the viewer's built-in save.

  const handleClear = useCallback(() => {
    if (stampState.blobUrl) URL.revokeObjectURL(stampState.blobUrl);
    setStampState({ file: null, blobUrl: null, viewerReady: false });
    setError(null);
  }, [stampState.blobUrl]);

  const viewerUrl = stampState.blobUrl
    ? `/pdfjs-annotation-viewer/web/viewer.html?file=${encodeURIComponent(stampState.blobUrl)}`
    : null;

  return (
    <div className={`space-y-6 ${className}`.trim()}>
      {!stampState.file && (
        <FileUploader
          accept={['application/pdf', '.pdf']}
          multiple={false}
          maxFiles={1}
          onFilesSelected={handleFilesSelected}
          onError={handleUploadError}
          disabled={isProcessing}
          label={tTools('uploadLabel') || 'Upload PDF File'}
          description={tTools('uploadDescription') || 'Drag and drop a PDF file here.'}
        />
      )}

      {error && (
        <div className="p-4 rounded-lg bg-red-50 border border-red-200 text-red-700" role="alert">
          <p className="text-sm">{error}</p>
        </div>
      )}

      {stampState.file && viewerUrl && (
        <>
          <Card variant="outlined">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <svg className="w-8 h-8 text-red-500" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6z" />
                  <path d="M14 2v6h6" fill="white" />
                </svg>
                <div>
                  <p className="text-sm font-medium">{stampState.file.name}</p>
                  <p className="text-xs text-gray-500">{(stampState.file.size / 1024 / 1024).toFixed(2)} MB</p>
                </div>
              </div>
              <Button variant="ghost" size="sm" onClick={handleClear} disabled={isProcessing}>
                {t('buttons.remove') || 'Remove'}
              </Button>
            </div>
          </Card>

          <Card variant="outlined" className="bg-blue-50 border-blue-200">
            <div className="flex gap-3">
              <svg className="w-5 h-5 text-blue-500 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div className="text-sm text-blue-700">
                <p className="font-medium mb-1">{tTools('instructionsTitle') || 'How to Add Stamps'}</p>
                <ol className="list-decimal list-inside space-y-1 text-blue-600">
                  <li>{tTools('instruction1') || 'Click the Stamp tool in the toolbar'}</li>
                  <li>{tTools('instruction2') || 'Click Add image to upload your stamp'}</li>
                  <li>{tTools('instruction3') || 'Click on the PDF to place the stamp'}</li>
                  <li>{tTools('instruction4') || 'Drag to resize or reposition'}</li>
                  <li>{tTools('instruction5') || 'Click the Export button in the toolbar above to download with stamps applied'}</li>
                </ol>
              </div>
            </div>
          </Card>

          <div className="border rounded-lg overflow-hidden">
            <iframe
              ref={iframeRef}
              src={viewerUrl}
              onLoad={handleIframeLoad}
              className="w-full bg-gray-100"
              style={{ height: '700px', border: 'none' }}
              title="PDF Stamp Editor"
            />
          </div>
        </>
      )}
    </div>
  );
}

export default StampsTool;
