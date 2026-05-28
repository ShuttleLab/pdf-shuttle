import { ImageResponse } from 'next/og';

export const dynamic = 'force-static';
export const revalidate = false;

export async function GET() {
  return new ImageResponse(
    (
      <div
        style={{
          width: '100%',
          height: '100%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          background: '#3b82f6',
          borderRadius: '96px',
        }}
      >
        <div
          style={{
            color: 'white',
            fontSize: 160,
            fontWeight: 800,
            letterSpacing: '-4px',
          }}
        >
          PDF
        </div>
      </div>
    ),
    { width: 512, height: 512 }
  );
}
