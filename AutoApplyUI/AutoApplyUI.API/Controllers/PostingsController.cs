using AutoApplyUI.API.ExternalServices.Applications;
using AutoApplyUI.API.ExternalServices.Postings;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace AutoApplyUI.API.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class PostingsController : ControllerBase
    {
        [HttpGet]
        [Route("retrieveAll")]
        public async Task<List<Posting>> GetPostings()
        {
            var x = new PostingsService();
            return await x.GetPostings();
        }

        [HttpGet]
        [Route("generateApplication")]
        public async Task<string> WriteCoverLetter([FromBody] string posting)
        {
            var x = new OpenAiService();
            return await x.WriteCoverLetter(posting);
        }
    }
}
