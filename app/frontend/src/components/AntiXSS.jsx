import DOMPurify from 'dompurify';

function SafeComponent({ userInput }) {
  const cleanInput = DOMPurify.sanitize(userInput);
  return <div dangerouslySetInnerHTML={{ __html: cleanInput }} />;
}
